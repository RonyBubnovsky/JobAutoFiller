import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import time

# Automation libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Constants ---
DATA_FILE = "user_settings.json"

class AutoApplierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Auto-Filler")
        self.root.geometry("550x500")
        
        # Variables linked to UI inputs
        self.form_data = {
            "First Name": tk.StringVar(),
            "Last Name": tk.StringVar(),
            "Email": tk.StringVar(),
            "Phone": tk.StringVar(),
            "LinkedIn URL": tk.StringVar(),
            "Website/Portfolio": tk.StringVar(),
            "Resume Path": tk.StringVar()
        }
        self.job_url = tk.StringVar()

        # Build UI and load data
        self.create_layout()
        self.load_saved_data()

    def create_layout(self):
        """Builds the UI layout."""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(main_frame, text="Candidate Settings", font=("Segoe UI", 12, "bold")).pack(pady=(0, 15))

        # Define required fields
        self.required_fields = ["First Name", "Last Name", "Email", "Phone", "Resume Path"]

        # Create input fields
        for label_text, var in self.form_data.items():
            row_frame = tk.Frame(main_frame)
            row_frame.pack(fill="x", pady=2)
            
            # Label with fixed width for alignment
            lbl = tk.Label(row_frame, text=label_text, width=16, anchor="w")
            lbl.pack(side="left")
            
            # Red asterisk for required fields, space placeholder for non-required
            if label_text in self.required_fields:
                asterisk = tk.Label(row_frame, text="*", fg="red", font=("Segoe UI", 10, "bold"))
            else:
                asterisk = tk.Label(row_frame, text=" ")
            asterisk.config(width=2, anchor="w")
            asterisk.pack(side="left")
            
            if label_text == "Resume Path":
                tk.Entry(row_frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=5)
                tk.Button(row_frame, text="Browse", command=self.browse_file).pack(side="right")
            else:
                tk.Entry(row_frame, textvariable=var).pack(side="left", fill="x", expand=True)

        # Separator line
        tk.Frame(main_frame, height=2, bd=1, relief="sunken").pack(fill="x", pady=20)

        # Job URL section
        url_frame = tk.Frame(main_frame)
        url_frame.pack(fill="x", pady=5)
        tk.Label(url_frame, text="Job Link:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Create entry with explicit clipboard support
        self.job_url_entry = tk.Entry(url_frame, textvariable=self.job_url, bg="#f0f8ff")
        self.job_url_entry.pack(fill="x", pady=5)
        
        # Bind Ctrl+V explicitly for paste support
        self.job_url_entry.bind('<Control-v>', self.paste_to_entry)
        self.job_url_entry.bind('<Control-V>', self.paste_to_entry)
        # Also bind right-click menu
        self.job_url_entry.bind('<Button-3>', self.show_paste_menu)

        # Run button
        btn = tk.Button(main_frame, text="Open & Fill Form", command=self.run_bot, 
                        bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), height=2)
        btn.pack(fill="x", pady=20)

    def paste_to_entry(self, event=None):
        """Handle paste operation explicitly."""
        try:
            # Get clipboard content
            clipboard_text = self.root.clipboard_get()
            # Get the widget that triggered the event
            widget = event.widget if event else self.job_url_entry
            # Delete selected text if any
            try:
                widget.delete("sel.first", "sel.last")
            except tk.TclError:
                pass  # No selection
            # Insert clipboard content at cursor position
            widget.insert("insert", clipboard_text)
            return "break"  # Prevent default handling
        except tk.TclError:
            pass  # Clipboard empty or unavailable
        return "break"

    def show_paste_menu(self, event):
        """Show right-click context menu with paste option."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Paste", command=lambda: self.paste_to_entry())
        menu.add_command(label="Clear", command=lambda: self.job_url.set(""))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def browse_file(self):
        """Opens file dialog to select resume."""
        filename = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx")])
        if filename:
            self.form_data["Resume Path"].set(filename)

    def load_saved_data(self):
        """Loads data from JSON file if it exists."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        if k in self.form_data:
                            self.form_data[k].set(v)
            except Exception:
                pass 

    def save_current_data(self):
        """Saves current inputs to JSON file."""
        data_to_save = {k: v.get() for k, v in self.form_data.items()}
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save settings: {e}")

    def validate_required_fields(self):
        """Check that all required fields are filled."""
        missing_fields = []
        for field_name in self.required_fields:
            value = self.form_data[field_name].get().strip()
            if not value:
                missing_fields.append(field_name)
        return missing_fields

    def run_bot(self):
        """Main automation logic."""
        # Validate required fields
        missing = self.validate_required_fields()
        if missing:
            fields_list = "\n- ".join(missing)
            messagebox.showwarning("Missing Required Fields", f"Please fill in the following required fields:\n- {fields_list}")
            return
        
        url = self.job_url.get()
        if not url:
            messagebox.showwarning("Missing Info", "Please enter a Job URL")
            return

        self.save_current_data() 

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(url)
            wait = WebDriverWait(driver, 15) # Increased wait time

            # --- STEP 1: FIND AND CLICK THE BUTTON ---
            print("Looking for Apply button...")
            try:
                # Multiple XPath options to find the Apply button
                button_xpaths = [
                    # Button element with exact or partial text
                    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
                    # Anchor/link styled as button
                    "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
                    # Div or span that acts as button
                    "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
                    "//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
                    # Any clickable element containing the text (broader search)
                    "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]",
                    # Common class patterns for apply buttons
                    "//*[contains(@class, 'apply') and contains(@class, 'btn')]",
                    "//*[contains(@class, 'apply-button')]",
                    "//*[contains(@id, 'apply')]",
                ]
                
                apply_btn = None
                for xpath in button_xpaths:
                    try:
                        apply_btn = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        if apply_btn and apply_btn.is_displayed():
                            print(f"Found button with xpath: {xpath}")
                            break
                    except:
                        continue
                
                if not apply_btn:
                    # Fallback: wait longer and try again with main xpath
                    time.sleep(3)
                    xpath_query = "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply for this job')]"
                    apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_query)))
                
                # Scroll into view (helps if button is at the bottom)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", apply_btn)
                time.sleep(1)

                # Try multiple click methods
                clicked = False
                
                # Method 1: Wait for clickable and standard click
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    apply_btn.click()
                    clicked = True
                    print("Button clicked (standard click).")
                except Exception as e1:
                    print(f"Standard click failed: {e1}")
                
                # Method 2: JavaScript click
                if not clicked:
                    try:
                        driver.execute_script("arguments[0].click();", apply_btn)
                        clicked = True
                        print("Button clicked (JS click).")
                    except Exception as e2:
                        print(f"JS click failed: {e2}")
                
                # Method 3: Action chains click
                if not clicked:
                    try:
                        from selenium.webdriver.common.action_chains import ActionChains
                        actions = ActionChains(driver)
                        actions.move_to_element(apply_btn).click().perform()
                        clicked = True
                        print("Button clicked (ActionChains).")
                    except Exception as e3:
                        print(f"ActionChains click failed: {e3}")
                
                if not clicked:
                    print("WARNING: Could not click the button with any method!")
                
                # Wait for form to load after clicking
                time.sleep(3)
                
            except Exception as e:
                print(f"Apply button not found or could not be clicked: {e}")
                # We continue anyway, in case the form is already open

            # --- STEP 2: SWITCH TO IFRAME IF EXISTS ---
            print("Checking for iframes...")
            try:
                # Try to find and switch to iframe containing the form
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                print(f"Found {len(iframes)} iframe(s)")
                
                switched_to_iframe = False
                for i, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        # Check if this iframe has form fields
                        test_elements = driver.find_elements(By.XPATH, "//input[@type='text' or @type='email' or @type='tel']")
                        if len(test_elements) > 0:
                            print(f"Switched to iframe {i} - found {len(test_elements)} input fields")
                            switched_to_iframe = True
                            break
                        else:
                            driver.switch_to.default_content()
                    except:
                        driver.switch_to.default_content()
                        continue
                
                if not switched_to_iframe:
                    print("No iframe with form found, staying in main content")
                    driver.switch_to.default_content()
            except Exception as e:
                print(f"Iframe check error: {e}")

            # --- STEP 3: WAIT FOR FORM TO OPEN ---
            print("Waiting for form fields...")
            # Wait for the form to fully load - look for common form elements
            form_loaded = False
            time.sleep(2)  # Give Angular time to render
            
            try:
                # Try multiple indicators that form is loaded
                form_indicators = [
                    "//input[@id='inputFirstName']",
                    "//input[@name='firstName']",
                    "//input[@type='text']",
                    "//input[@type='email']",
                    "//form",
                ]
                for indicator in form_indicators:
                    try:
                        elements = driver.find_elements(By.XPATH, indicator)
                        if len(elements) > 0:
                            form_loaded = True
                            print(f"Form loaded (found {len(elements)} elements matching: {indicator})")
                            break
                    except:
                        continue
                
                if not form_loaded:
                    # Give extra time for Angular/React forms to render
                    time.sleep(3)
                    print("Waited extra time for form to render...")
            except:
                print("Form did not open or form elements not found.")

            # Debug: Print all visible input fields
            print("\n--- DEBUG: Scanning all input fields ---")
            try:
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                print(f"Found {len(all_inputs)} input elements total")
                for inp in all_inputs[:15]:  # Show first 15
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

            # --- STEP 4: FILL FIELDS ---
            # Updated field mapping based on actual HTML structure
            fields_config = [
                # (Label in app, list of (selector_type, selector_value) tuples)
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
                value = self.form_data[label].get()
                if not value:
                    continue
                    
                filled = False
                for selector_type, selector_value in selectors:
                    try:
                        inp = driver.find_element(selector_type, selector_value)
                        if inp.is_displayed():
                            inp.clear()
                            inp.send_keys(value)
                            print(f"Filled '{label}' using {selector_type}='{selector_value}'")
                            filled = True
                            break
                    except Exception as e:
                        continue
                
                if not filled:
                    print(f"Could not fill field: {label}")

            # --- STEP 4: UPLOAD FILE ---
            resume = self.form_data["Resume Path"].get()
            if resume and os.path.exists(resume):
                uploaded = False
                
                # Try multiple methods to find file input
                file_selectors = [
                    (By.XPATH, "//input[@type='file']"),
                    (By.XPATH, "//input[contains(@id, 'file')]"),
                    (By.XPATH, "//input[contains(@name, 'resume')]"),
                    (By.XPATH, "//input[contains(@name, 'file')]"),
                    (By.XPATH, "//input[contains(@accept, 'pdf')]"),
                ]
                
                for selector_type, selector_value in file_selectors:
                    try:
                        file_input = driver.find_element(selector_type, selector_value)
                        file_input.send_keys(resume)
                        print(f"Resume uploaded using {selector_value}")
                        uploaded = True
                        break
                    except:
                        continue
                
                # If no file input found, try clicking "Attach Resume" button first
                if not uploaded:
                    try:
                        attach_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Attach Resume') or contains(text(), 'attach resume')]")
                        attach_btn.click()
                        time.sleep(1)
                        # Now try to find the file input again
                        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                        file_input.send_keys(resume)
                        print("Resume uploaded after clicking Attach button.")
                        uploaded = True
                    except Exception as e:
                        print(f"Could not upload file: {e}")

            print("Automation finished. Browser stays open for manual submit.")

        except Exception as e:
            messagebox.showerror("Automation Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoApplierGUI(root)
    root.mainloop()