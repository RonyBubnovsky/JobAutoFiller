"""Modern entry input component."""

import customtkinter as ctk
import tkinter as tk
from src.gui.theme import Colors, Fonts


class ModernEntry(ctk.CTkFrame):
    """Modern input field with floating label effect and validation."""
    
    def __init__(self, master, label: str, variable: tk.StringVar, 
                 required: bool = False, placeholder: str = "", **kwargs):
        super().__init__(master, fg_color=Colors.TRANSPARENT)
        
        self.variable = variable
        self.required = required
        self.is_valid = True
        
        # Label row with required indicator
        label_frame = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        label_frame.pack(fill="x", pady=(0, 4))
        
        self.label = ctk.CTkLabel(
            label_frame,
            text=label,
            font=Fonts.label(),
            text_color=Colors.TEXT_SECONDARY,
            anchor="w"
        )
        self.label.pack(side="left")
        
        if required:
            required_badge = ctk.CTkLabel(
                label_frame,
                text="Required",
                font=Fonts.hint(),
                text_color=Colors.ERROR,
                fg_color=Colors.ERROR_BG,
                corner_radius=6,
                padx=6,
                pady=2
            )
            required_badge.pack(side="left", padx=(8, 0))
        
        # Entry field
        self.entry = ctk.CTkEntry(
            self,
            textvariable=variable,
            placeholder_text=placeholder,
            height=44,
            corner_radius=10,
            border_width=2,
            border_color=Colors.BORDER_DEFAULT,
            fg_color=Colors.BG_INPUT,
            font=Fonts.body(),
            **kwargs
        )
        self.entry.pack(fill="x")
        
        # Bind focus events for interactive border
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
    def _on_focus_in(self, event):
        """Highlight border on focus."""
        self.entry.configure(border_color=Colors.PRIMARY_LIGHT)
        self.label.configure(text_color=Colors.PRIMARY_LIGHT)
        
    def _on_focus_out(self, event):
        """Reset border on blur."""
        if self.required and not self.variable.get().strip():
            self.entry.configure(border_color=Colors.ERROR)
            self.label.configure(text_color=Colors.ERROR)
        else:
            self.entry.configure(border_color=Colors.BORDER_DEFAULT)
            self.label.configure(text_color=Colors.TEXT_SECONDARY)
    
    def get_entry(self):
        """Return the internal entry widget."""
        return self.entry
