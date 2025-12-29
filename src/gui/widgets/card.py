"""Modern card component."""

import customtkinter as ctk
from src.gui.theme import Colors


class ModernCard(ctk.CTkFrame):
    """A modern card component with subtle shadow effect."""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=16,
            fg_color=Colors.BG_CARD,
            border_width=1,
            border_color=Colors.BORDER_CARD,
            **kwargs
        )
