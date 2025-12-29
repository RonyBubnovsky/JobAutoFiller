"""Animated button component."""

import customtkinter as ctk
from src.gui.theme import Colors, Fonts


class AnimatedButton(ctk.CTkButton):
    """Button with hover animations and modern styling."""
    
    def __init__(self, master, **kwargs):
        # Modern gradient-like colors
        default_kwargs = {
            "corner_radius": 12,
            "height": 50,
            "font": Fonts.button(),
            "hover_color": Colors.PRIMARY_HOVER,
            "fg_color": Colors.PRIMARY,
        }
        default_kwargs.update(kwargs)
        super().__init__(master, **default_kwargs)
        
        # Bind hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event=None):
        """Scale up effect on hover."""
        self.configure(font=Fonts.button_hover())
        
    def _on_leave(self, event=None):
        """Reset scale on leave."""
        self.configure(font=Fonts.button())
