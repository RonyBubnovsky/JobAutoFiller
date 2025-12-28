import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class BrowserAutomation:
    """Handles all browser automation for job application filling."""
    
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def start_browser(self, url: str) -> None:
        """Initialize browser and navigate to URL."""
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 15)
    
    def click_apply_button(self) -> bool:
        """Find and click the Apply button."""
        print("Looking for Apply button...")
        
        button_xpaths = [
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
            "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
            "//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
            "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
            "//*[contains(@class, 'apply') and contains(@class, 'btn')]",
            "//*[contains(@class, 'apply-button')]",
            "//*[contains(@id, 'apply')]",
        ]
        
        apply_btn = None
        found_xpath = None
        
        for xpath in button_xpaths:
            try:
                apply_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                if apply_btn and apply_btn.is_displayed():
                    print(f"Found button with xpath: {xpath}")
                    found_xpath = xpath
                    break
            except:
                continue
        
        if not apply_btn:
            time.sleep(3)
            xpath_query = "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]"
            try:
                apply_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_query)))
                found_xpath = xpath_query
            except:
                print("Apply button not found")
                return False
        
        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", apply_btn)
        time.sleep(1)
        
        # Try multiple click methods
        clicked = self._try_click(apply_btn, found_xpath)
        
        if clicked:
            time.sleep(3)
        
        return clicked
    
    def _try_click(self, element, xpath: str) -> bool:
        """Try multiple methods to click an element."""
        # Method 1: Standard click
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            print("Button clicked (standard click).")
            return True
        except Exception as e1:
            print(f"Standard click failed: {e1}")
        
        # Method 2: JavaScript click
        try:
            self.driver.execute_script("arguments[0].click();", element)
            print("Button clicked (JS click).")
            return True
        except Exception as e2:
            print(f"JS click failed: {e2}")
        
        # Method 3: Action chains click
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
            print("Button clicked (ActionChains).")
            return True
        except Exception as e3:
            print(f"ActionChains click failed: {e3}")
        
        print("WARNING: Could not click the button with any method!")
        return False
    
    def switch_to_form_iframe(self) -> bool:
        """Check for iframes and switch to one containing the form."""
        print("Checking for iframes...")
        
        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            print(f"Found {len(iframes)} iframe(s)")
            
            for i, iframe in enumerate(iframes):
                try:
                    self.driver.switch_to.frame(iframe)
                    test_elements = self.driver.find_elements(
                        By.XPATH, "//input[@type='text' or @type='email' or @type='tel']"
                    )
                    if len(test_elements) > 0:
                        print(f"Switched to iframe {i} - found {len(test_elements)} input fields")
                        return True
                    else:
                        self.driver.switch_to.default_content()
                except:
                    self.driver.switch_to.default_content()
                    continue
            
            print("No iframe with form found, staying in main content")
            self.driver.switch_to.default_content()
            return False
            
        except Exception as e:
            print(f"Iframe check error: {e}")
            return False
    
    def wait_for_form(self) -> bool:
        """Wait for form to load."""
        print("Waiting for form fields...")
        time.sleep(2)
        
        form_indicators = [
            "//input[@id='inputFirstName']",
            "//input[@name='firstName']",
            "//input[@type='text']",
            "//input[@type='email']",
            "//form",
        ]
        
        for indicator in form_indicators:
            try:
                elements = self.driver.find_elements(By.XPATH, indicator)
                if len(elements) > 0:
                    print(f"Form loaded (found {len(elements)} elements matching: {indicator})")
                    return True
            except:
                continue
        
        time.sleep(3)
        print("Waited extra time for form to render...")
        return False
    
    def debug_scan_inputs(self) -> None:
        """Print all visible input fields for debugging."""
        print("\n--- DEBUG: Scanning all input fields ---")
        try:
            all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"Found {len(all_inputs)} input elements total")
            for inp in all_inputs[:15]:
                try:
                    inp_id = inp.get_attribute("id") or ""
                    inp_name = inp.get_attribute("name") or ""
                    inp_type = inp.get_attribute("type") or ""
                    inp_aria = inp.get_attribute("aria-label") or ""
                    if inp_id or inp_name:
                        print(f"  Input: id='{inp_id}', name='{inp_name}', type='{inp_type}', aria-label='{inp_aria}'")
                except:
                    pass
        except Exception as e:
            print(f"Debug scan error: {e}")
        print("--- END DEBUG ---\n")
    
    def fill_form_fields(self, form_data: dict) -> None:
        """Fill in the form fields."""
        fields_config = [
            ("First Name", [
                (By.ID, "inputFirstName"),
                (By.NAME, "firstName"),
                (By.XPATH, "//input[@aria-label='First name']"),
                (By.XPATH, "//input[contains(@name, 'first')]"),
                (By.XPATH, "//input[contains(@id, 'first') or contains(@id, 'First')]"),
                (By.XPATH, "//input[contains(@autocomplete, 'given-name')]"),
            ]),
            ("Last Name", [
                (By.ID, "inputLastName"),
                (By.NAME, "lastName"),
                (By.XPATH, "//input[@aria-label='Last name']"),
                (By.XPATH, "//input[contains(@name, 'last')]"),
                (By.XPATH, "//input[contains(@id, 'last') or contains(@id, 'Last')]"),
                (By.XPATH, "//input[contains(@autocomplete, 'family-name')]"),
            ]),
            ("Email", [
                (By.ID, "inputEmail"),
                (By.NAME, "email"),
                (By.XPATH, "//input[@type='email']"),
                (By.XPATH, "//input[@aria-label='Email']"),
                (By.XPATH, "//input[contains(@autocomplete, 'email')]"),
            ]),
            ("Phone", [
                (By.ID, "inputTel"),
                (By.NAME, "phone"),
                (By.XPATH, "//input[@type='tel']"),
                (By.XPATH, "//input[@aria-label='Phone']"),
                (By.XPATH, "//input[contains(@autocomplete, 'tel')]"),
            ]),
            ("LinkedIn URL", [
                (By.ID, "linkedin"),
                (By.NAME, "linkedin"),
                (By.XPATH, "//input[@aria-label='LinkedIn Profile URL']"),
                (By.XPATH, "//input[contains(@name, 'linkedin')]"),
                (By.XPATH, "//input[contains(@id, 'linkedin')]"),
            ]),
            ("Website/Portfolio", [
                (By.ID, "inputLink"),
                (By.NAME, "websiteUrl"),
                (By.XPATH, "//input[@aria-label='Personal website']"),
                (By.XPATH, "//input[contains(@name, 'website')]"),
            ]),
        ]
        
        for label, selectors in fields_config:
            value = form_data[label].get()
            if not value:
                continue
            
            filled = False
            for selector_type, selector_value in selectors:
                try:
                    inp = self.driver.find_element(selector_type, selector_value)
                    if inp.is_displayed():
                        inp.clear()
                        inp.send_keys(value)
                        print(f"Filled '{label}' using {selector_type}='{selector_value}'")
                        filled = True
                        break
                except:
                    continue
            
            if not filled:
                print(f"Could not fill field: {label}")
    
    def upload_resume(self, resume_path: str) -> bool:
        """Upload resume file."""
        if not resume_path or not os.path.exists(resume_path):
            return False
        
        file_selectors = [
            (By.XPATH, "//input[@type='file']"),
            (By.XPATH, "//input[contains(@id, 'file')]"),
            (By.XPATH, "//input[contains(@name, 'resume')]"),
            (By.XPATH, "//input[contains(@name, 'file')]"),
            (By.XPATH, "//input[contains(@accept, 'pdf')]"),
        ]
        
        for selector_type, selector_value in file_selectors:
            try:
                file_input = self.driver.find_element(selector_type, selector_value)
                file_input.send_keys(resume_path)
                print(f"Resume uploaded using {selector_value}")
                return True
            except:
                continue
        
        # Try clicking "Attach Resume" button first
        try:
            attach_btn = self.driver.find_element(
                By.XPATH, 
                "//*[contains(text(), 'Attach Resume') or contains(text(), 'attach resume')]"
            )
            attach_btn.click()
            time.sleep(1)
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(resume_path)
            print("Resume uploaded after clicking Attach button.")
            return True
        except Exception as e:
            print(f"Could not upload file: {e}")
            return False
