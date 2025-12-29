"""Personal information card component."""

import customtkinter as ctk
import tkinter as tk
from typing import Dict
from src.gui.theme import Colors, Fonts
from src.gui.widgets import ModernCard, ModernEntry


class PersonalInfoCard(ctk.CTkFrame):
    """Card for personal information input."""
    
    def __init__(self, master, form_data: Dict[str, tk.StringVar]):
        super().__init__(master, fg_color=Colors.TRANSPARENT)
        
        self.form_data = form_data
        self._create_layout()
        
    def _create_layout(self):
        """Create the personal info card layout."""
        card = ModernCard(self)
        card.pack(fill="x")
        
        inner = ctk.CTkFrame(card, fg_color=Colors.TRANSPARENT)
        inner.pack(fill="x", padx=20, pady=20)
        
        # Card header
        header = ctk.CTkLabel(
            inner,
            text="👤  Personal Information",
            font=Fonts.header(),
            anchor="w"
        )
        header.pack(fill="x", pady=(0, 16))
        
        # Two-column layout for name
        name_row = ctk.CTkFrame(inner, fg_color=Colors.TRANSPARENT)
        name_row.pack(fill="x", pady=(0, 12))
        
        # First Name
        first_name_frame = ctk.CTkFrame(name_row, fg_color=Colors.TRANSPARENT)
        first_name_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.first_name_entry = ModernEntry(
            first_name_frame,
            "First Name",
            self.form_data["First Name"],
            required=True,
            placeholder="John"
        )
        self.first_name_entry.pack(fill="x")
        
        # Last Name
        last_name_frame = ctk.CTkFrame(name_row, fg_color=Colors.TRANSPARENT)
        last_name_frame.pack(side="right", fill="x", expand=True, padx=(8, 0))
        self.last_name_entry = ModernEntry(
            last_name_frame,
            "Last Name",
            self.form_data["Last Name"],
            required=True,
            placeholder="Doe"
        )
        self.last_name_entry.pack(fill="x")
        
        # Email
        self.email_entry = ModernEntry(
            inner,
            "Email Address",
            self.form_data["Email"],
            required=True,
            placeholder="john.doe@example.com"
        )
        self.email_entry.pack(fill="x", pady=(0, 12))
        
        # Phone
        self.phone_entry = ModernEntry(
            inner,
            "Phone Number",
            self.form_data["Phone"],
            required=True,
            placeholder="+1 (555) 123-4567"
        )
        self.phone_entry.pack(fill="x")
