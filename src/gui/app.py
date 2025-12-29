"""Main application GUI class."""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading

from src.constants import REQUIRED_FIELDS
from src.data_manager import load_saved_data, save_current_data
from src.browser_automation import BrowserAutomation

from src.gui.theme import setup_theme
from src.gui.validators import is_valid_comeet_url, validate_required_fields
from src.gui.widgets import AnimatedButton, StatusBar
from src.gui.cards import (
    HeaderCard,
    PersonalInfoCard,
    LinksCard,
    ResumeCard,
    JobUrlCard,
)


class AutoApplierGUI:
    """Modern GUI class for the Job Application Auto-Filler."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Job Auto-Filler")
        self.root.geometry("620x820")
        self.root.minsize(550, 700)
        
        # Initialize theme
        setup_theme()
        
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
        self.required_fields = REQUIRED_FIELDS
        
        # Build UI
        self._create_layout()
        
        # Load saved data
        load_saved_data(self.form_data)
        
        # Theme toggle state
        self.dark_mode = True
        
    def _create_layout(self) -> None:
        """Builds the modern UI layout."""
        # Main scrollable container
        self.main_container = ctk.CTkScrollableFrame(
            self.root,
            fg_color="transparent",
            scrollbar_button_color=("gray70", "gray30")
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self.header = HeaderCard(self.main_container, self._toggle_theme)
        self.header.pack(fill="x", pady=(0, 20))
        
        # Personal Info Card
        self.personal_info_card = PersonalInfoCard(self.main_container, self.form_data)
        self.personal_info_card.pack(fill="x", pady=(0, 16))
        
        # Links Card
        self.links_card = LinksCard(self.main_container, self.form_data)
        self.links_card.pack(fill="x", pady=(0, 16))
        
        # Resume Card
        self.resume_card = ResumeCard(self.main_container, self.form_data)
        self.resume_card.pack(fill="x", pady=(0, 16))
        
        # Job URL Card
        self.job_url_card = JobUrlCard(self.main_container, self.job_url, self.root)
        self.job_url_card.pack(fill="x", pady=(0, 16))
        
        # Status Bar
        self.status_bar = StatusBar(self.main_container)
        self.status_bar.pack(fill="x", pady=(16, 0))
        
        # Action Button
        self._create_action_button()
        
    def _create_action_button(self) -> None:
        """Create the main action button."""
        self.run_btn = AnimatedButton(
            self.main_container,
            text="🚀  Open & Fill Application",
            command=self._run_bot
        )
        self.run_btn.pack(fill="x", pady=(20, 0))
        
    def _toggle_theme(self) -> bool:
        """Toggle between light and dark mode.
        
        Returns:
            True if now in dark mode, False if in light mode.
        """
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        return self.dark_mode
    
    def _run_bot(self) -> None:
        """Main automation logic."""
        # Validate required fields
        missing = validate_required_fields(self.form_data, self.required_fields)
        if missing:
            fields_list = "\n• ".join(missing)
            messagebox.showwarning(
                "Missing Required Fields",
                f"Please fill in the following required fields:\n\n• {fields_list}"
            )
            self.status_bar.set_error("Missing required fields")
            return
        
        url = self.job_url.get().strip()
        if not url:
            messagebox.showwarning("Missing Info", "Please enter a Job URL")
            self.status_bar.set_error("No job URL provided")
            return
        
        if not is_valid_comeet_url(url):
            messagebox.showwarning(
                "Invalid URL",
                "Please enter a valid Comeet job URL.\n\n"
                "Example: https://www.comeet.com/jobs/company/ID/job-title/ID"
            )
            self.status_bar.set_error("Invalid Comeet URL")
            return
        
        # Disable button and show loading
        self.run_btn.configure(state="disabled", text="Processing...")
        self.status_bar.set_loading("Starting automation...")
        
        # Save data
        save_current_data(self.form_data)
        
        # Run automation in thread to keep UI responsive
        thread = threading.Thread(target=self._execute_automation, daemon=True)
        thread.start()
        
    def _execute_automation(self) -> None:
        """Execute the automation in a separate thread."""
        try:
            self.root.after(0, lambda: self.status_bar.set_loading("Opening browser..."))
            
            automation = BrowserAutomation()
            automation.start_browser(self.job_url.get())
            
            self.root.after(0, lambda: self.status_bar.set_loading("Clicking apply button..."))
            automation.click_apply_button()
            
            self.root.after(0, lambda: self.status_bar.set_loading("Switching to form..."))
            automation.switch_to_form_iframe()
            
            self.root.after(0, lambda: self.status_bar.set_loading("Waiting for form..."))
            automation.wait_for_form()
            
            automation.debug_scan_inputs()
            
            self.root.after(0, lambda: self.status_bar.set_loading("Filling form fields..."))
            automation.fill_form_fields(self.form_data)
            
            self.root.after(0, lambda: self.status_bar.set_loading("Uploading resume..."))
            resume_path = self.form_data["Resume Path"].get()
            automation.upload_resume(resume_path)
            
            self.root.after(0, lambda: self.status_bar.set_success("Form filled successfully!"))
            print("Automation finished. Browser stays open for manual submit.")
            
        except Exception as e:
            self.root.after(0, lambda: self.status_bar.set_error(f"Error: {str(e)[:50]}"))
            self.root.after(0, lambda: messagebox.showerror("Automation Error", str(e)))
            
        finally:
            self.root.after(0, lambda: self.run_btn.configure(
                state="normal", 
                text="🚀  Open & Fill Application"
            ))
