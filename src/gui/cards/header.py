"""Header card component."""

import customtkinter as ctk
from typing import Callable
from src.gui.theme import Colors, Fonts


class HeaderCard(ctk.CTkFrame):
    """Header section with title and theme toggle."""
    
    def __init__(self, master, on_theme_toggle: Callable):
        super().__init__(master, fg_color=Colors.TRANSPARENT)
        
        self.on_theme_toggle = on_theme_toggle
        self._create_layout()
        
    def _create_layout(self):
        """Create the header layout."""
        # Left side - Logo and title
        left = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        left.pack(side="left", fill="y")
        
        logo_frame = ctk.CTkFrame(
            left,
            width=48,
            height=48,
            corner_radius=12,
            fg_color=Colors.PRIMARY
        )
        logo_frame.pack(side="left")
        logo_frame.pack_propagate(False)
        
        logo_text = ctk.CTkLabel(
            logo_frame,
            text="🚀",
            font=Fonts.icon_large()
        )
        logo_text.pack(expand=True)
        
        title_frame = ctk.CTkFrame(left, fg_color=Colors.TRANSPARENT)
        title_frame.pack(side="left", padx=(12, 0))
        
        title = ctk.CTkLabel(
            title_frame,
            text="Job Auto-Filler",
            font=Fonts.title(),
            anchor="w"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Automate your job applications",
            font=Fonts.subtitle(),
            text_color=Colors.TEXT_MUTED,
            anchor="w"
        )
        subtitle.pack(anchor="w")
        
        # Right side - Theme toggle
        self.theme_btn = ctk.CTkButton(
            self,
            text="☀️",
            width=40,
            height=40,
            corner_radius=10,
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35"),
            font=Fonts.icon(),
            command=self._handle_theme_toggle
        )
        self.theme_btn.pack(side="right")
        
    def _handle_theme_toggle(self):
        """Handle theme toggle and update button icon."""
        is_dark = self.on_theme_toggle()
        self.theme_btn.configure(text="☀️" if is_dark else "🌙")
