import tkinter as tk
from tkinter import filedialog, messagebox

from src.constants import REQUIRED_FIELDS
from src.data_manager import load_saved_data, save_current_data
from src.browser_automation import BrowserAutomation


class AutoApplierGUI:
    """Main GUI class for the Job Application Auto-Filler."""
    
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
        self.required_fields = REQUIRED_FIELDS

        # Build UI and load data
        self._create_layout()
        load_saved_data(self.form_data)

    def _create_layout(self) -> None:
        """Builds the UI layout."""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            main_frame, 
            text="Candidate Settings", 
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(0, 15))

        # Create input fields
        for label_text, var in self.form_data.items():
            self._create_field_row(main_frame, label_text, var)

        # Separator line
        tk.Frame(main_frame, height=2, bd=1, relief="sunken").pack(fill="x", pady=20)

        # Job URL section
        self._create_job_url_section(main_frame)

        # Run button
        btn = tk.Button(
            main_frame, 
            text="Open & Fill Form", 
            command=self._run_bot,
            bg="#4CAF50", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            height=2
        )
        btn.pack(fill="x", pady=20)

    def _create_field_row(self, parent: tk.Frame, label_text: str, var: tk.StringVar) -> None:
        """Create a single field row with label and entry."""
        row_frame = tk.Frame(parent)
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
            tk.Button(row_frame, text="Browse", command=self._browse_file).pack(side="right")
        else:
            tk.Entry(row_frame, textvariable=var).pack(side="left", fill="x", expand=True)

    def _create_job_url_section(self, parent: tk.Frame) -> None:
        """Create the job URL input section."""
        url_frame = tk.Frame(parent)
        url_frame.pack(fill="x", pady=5)
        tk.Label(url_frame, text="Job Link:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Create entry with explicit clipboard support
        self.job_url_entry = tk.Entry(url_frame, textvariable=self.job_url, bg="#f0f8ff")
        self.job_url_entry.pack(fill="x", pady=5)
        
        # Bind Ctrl+V explicitly for paste support
        self.job_url_entry.bind('<Control-v>', self._paste_to_entry)
        self.job_url_entry.bind('<Control-V>', self._paste_to_entry)
        # Also bind right-click menu
        self.job_url_entry.bind('<Button-3>', self._show_paste_menu)

    def _paste_to_entry(self, event=None) -> str:
        """Handle paste operation explicitly."""
        try:
            clipboard_text = self.root.clipboard_get()
            widget = event.widget if event else self.job_url_entry
            try:
                widget.delete("sel.first", "sel.last")
            except tk.TclError:
                pass
            widget.insert("insert", clipboard_text)
            return "break"
        except tk.TclError:
            pass
        return "break"

    def _show_paste_menu(self, event) -> None:
        """Show right-click context menu with paste option."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Paste", command=lambda: self._paste_to_entry())
        menu.add_command(label="Clear", command=lambda: self.job_url.set(""))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _browse_file(self) -> None:
        """Opens file dialog to select resume."""
        filename = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx")])
        if filename:
            self.form_data["Resume Path"].set(filename)

    def _validate_required_fields(self) -> list:
        """Check that all required fields are filled."""
        missing_fields = []
        for field_name in self.required_fields:
            value = self.form_data[field_name].get().strip()
            if not value:
                missing_fields.append(field_name)
        return missing_fields

    def _run_bot(self) -> None:
        """Main automation logic."""
        # Validate required fields
        missing = self._validate_required_fields()
        if missing:
            fields_list = "\n- ".join(missing)
            messagebox.showwarning(
                "Missing Required Fields", 
                f"Please fill in the following required fields:\n- {fields_list}"
            )
            return
        
        url = self.job_url.get()
        if not url:
            messagebox.showwarning("Missing Info", "Please enter a Job URL")
            return

        save_current_data(self.form_data)

        try:
            automation = BrowserAutomation()
            automation.start_browser(url)
            
            # Step 1: Click Apply button
            automation.click_apply_button()
            
            # Step 2: Switch to iframe if exists
            automation.switch_to_form_iframe()
            
            # Step 3: Wait for form
            automation.wait_for_form()
            
            # Debug: scan inputs
            automation.debug_scan_inputs()
            
            # Step 4: Fill fields
            automation.fill_form_fields(self.form_data)
            
            # Step 5: Upload resume
            resume_path = self.form_data["Resume Path"].get()
            automation.upload_resume(resume_path)
            
            print("Automation finished. Browser stays open for manual submit.")

        except Exception as e:
            messagebox.showerror("Automation Error", str(e))
