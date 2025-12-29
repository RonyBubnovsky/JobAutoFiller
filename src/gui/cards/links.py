"""Online presence links card component."""

import customtkinter as ctk
import tkinter as tk
from typing import Dict
from src.gui.theme import Colors, Fonts
from src.gui.widgets import ModernCard, ModernEntry


class LinksCard(ctk.CTkFrame):
    """Card for LinkedIn and portfolio links."""
    
    def __init__(self, master, form_data: Dict[str, tk.StringVar]):
        super().__init__(master, fg_color=Colors.TRANSPARENT)
        
        self.form_data = form_data
        self._create_layout()
        
    def _create_layout(self):
        """Create the links card layout."""
        card = ModernCard(self)
        card.pack(fill="x")
        
        inner = ctk.CTkFrame(card, fg_color=Colors.TRANSPARENT)
        inner.pack(fill="x", padx=20, pady=20)
        
        # Card header
        header = ctk.CTkLabel(
            inner,
            text="🔗  Online Presence",
            font=Fonts.header(),
            anchor="w"
        )
        header.pack(fill="x", pady=(0, 16))
        
        # LinkedIn
        self.linkedin_entry = ModernEntry(
            inner,
            "LinkedIn URL",
            self.form_data["LinkedIn URL"],
            required=False,
            placeholder="https://linkedin.com/in/yourprofile"
        )
        self.linkedin_entry.pack(fill="x", pady=(0, 12))
        
        # Portfolio
        self.portfolio_entry = ModernEntry(
            inner,
            "Website / Portfolio",
            self.form_data["Website/Portfolio"],
            required=False,
            placeholder="https://yourwebsite.com"
        )
        self.portfolio_entry.pack(fill="x")
