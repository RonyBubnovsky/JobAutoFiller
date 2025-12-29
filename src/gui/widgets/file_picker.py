"""File picker component."""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from src.gui.theme import Colors, Fonts


class FilePickerEntry(ctk.CTkFrame):
    """Modern file picker with drag & drop styling."""
    
    def __init__(self, master, label: str, variable: tk.StringVar, 
                 required: bool = False, filetypes: list = None):
        super().__init__(master, fg_color=Colors.TRANSPARENT)
        
        self.variable = variable
        self.filetypes = filetypes or [("All Files", "*.*")]
        
        # Label with required indicator
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
        
        # File picker container
        self.picker_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=2,
            border_color=Colors.BORDER_DEFAULT,
            fg_color=("gray98", "gray20"),
            height=80
        )
        self.picker_frame.pack(fill="x")
        self.picker_frame.pack_propagate(False)
        
        # Inner content
        inner = ctk.CTkFrame(self.picker_frame, fg_color=Colors.TRANSPARENT)
        inner.pack(expand=True, fill="both", padx=16, pady=12)
        
        # Icon and text row
        top_row = ctk.CTkFrame(inner, fg_color=Colors.TRANSPARENT)
        top_row.pack(fill="x")
        
        self.icon_label = ctk.CTkLabel(
            top_row,
            text="📄",
            font=ctk.CTkFont(size=20)
        )
        self.icon_label.pack(side="left")
        
        self.file_label = ctk.CTkLabel(
            top_row,
            text="No file selected",
            font=Fonts.subtitle(),
            text_color=Colors.TEXT_MUTED,
            anchor="w"
        )
        self.file_label.pack(side="left", padx=(8, 0), fill="x", expand=True)
        
        # Browse button
        self.browse_btn = ctk.CTkButton(
            top_row,
            text="Browse",
            width=90,
            height=32,
            corner_radius=8,
            font=Fonts.subtitle(),
            fg_color=Colors.BG_BUTTON_SECONDARY,
            hover_color=Colors.BG_BUTTON_SECONDARY_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            command=self._browse_file
        )
        self.browse_btn.pack(side="right")
        
        # Supported formats hint
        hint = ctk.CTkLabel(
            inner,
            text="Supported: PDF, DOCX",
            font=Fonts.small(),
            text_color=Colors.TEXT_HINT
        )
        hint.pack(anchor="w", pady=(4, 0))
        
        # Track variable changes
        self.variable.trace_add("write", self._update_display)
        self._update_display()
        
    def _browse_file(self):
        """Open file dialog."""
        filename = filedialog.askopenfilename(filetypes=self.filetypes)
        if filename:
            self.variable.set(filename)
            
    def _update_display(self, *args):
        """Update the display when file changes."""
        path = self.variable.get()
        if path:
            # Show just filename, not full path
            filename = path.split("/")[-1].split("\\")[-1]
            self.file_label.configure(text=filename, text_color=Colors.TEXT_PRIMARY)
            self.icon_label.configure(text="✅")
            self.picker_frame.configure(border_color=Colors.SUCCESS_LIGHT)
        else:
            self.file_label.configure(text="No file selected", text_color=Colors.TEXT_MUTED)
            self.icon_label.configure(text="📄")
            self.picker_frame.configure(border_color=Colors.BORDER_DEFAULT)
