"""Resume upload card component."""

import customtkinter as ctk
import tkinter as tk
from typing import Dict
from src.gui.theme import Colors, Fonts
from src.gui.widgets import ModernCard, FilePickerEntry


class ResumeCard(ctk.CTkFrame):
    """Card for resume file upload."""
    
    def __init__(self, master, form_data: Dict[str, tk.StringVar]):
        super().__init__(master, fg_color=Colors.TRANSPARENT)
        
        self.form_data = form_data
        self._create_layout()
        
    def _create_layout(self):
        """Create the resume card layout."""
        card = ModernCard(self)
        card.pack(fill="x")
        
        inner = ctk.CTkFrame(card, fg_color=Colors.TRANSPARENT)
        inner.pack(fill="x", padx=20, pady=20)
        
        # Card header
        header = ctk.CTkLabel(
            inner,
            text="📎  Resume",
            font=Fonts.header(),
            anchor="w"
        )
        header.pack(fill="x", pady=(0, 16))
        
        # File picker
        self.resume_picker = FilePickerEntry(
            inner,
            "Resume File",
            self.form_data["Resume Path"],
            required=True,
            filetypes=[("Documents", "*.pdf *.docx")]
        )
        self.resume_picker.pack(fill="x")
