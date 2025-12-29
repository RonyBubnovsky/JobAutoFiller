"""Job URL input card component."""

import customtkinter as ctk
import tkinter as tk
from typing import Callable
from src.gui.theme import Colors, Fonts
from src.gui.widgets import ModernCard
from src.gui.validators import is_valid_comeet_url


class JobUrlCard(ctk.CTkFrame):
    """Card for job URL input with Comeet validation."""
    
    def __init__(self, master, job_url: tk.StringVar, root: tk.Tk):
        super().__init__(master, fg_color=Colors.TRANSPARENT)
        
        self.job_url = job_url
        self.root = root
        self._create_layout()
        
    def _create_layout(self):
        """Create the job URL card layout."""
        card = ModernCard(self)
        card.pack(fill="x")
        
        inner = ctk.CTkFrame(card, fg_color=Colors.TRANSPARENT)
        inner.pack(fill="x", padx=20, pady=20)
        
        # Card header with paste button
        header_row = ctk.CTkFrame(inner, fg_color=Colors.TRANSPARENT)
        header_row.pack(fill="x", pady=(0, 16))
        
        header = ctk.CTkLabel(
            header_row,
            text="🎯  Job Application",
            font=Fonts.header(),
            anchor="w"
        )
        header.pack(side="left")
        
        paste_btn = ctk.CTkButton(
            header_row,
            text="📋 Paste",
            width=80,
            height=28,
            corner_radius=8,
            font=Fonts.small(),
            fg_color=Colors.BG_BUTTON_SECONDARY,
            hover_color=Colors.BG_BUTTON_SECONDARY_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            command=self._paste_url
        )
        paste_btn.pack(side="right")
        
        # URL Entry
        self.url_entry = ctk.CTkEntry(
            inner,
            textvariable=self.job_url,
            placeholder_text="Paste the job application URL here...",
            height=50,
            corner_radius=10,
            border_width=2,
            border_color=Colors.BORDER_DEFAULT,
            fg_color=Colors.BG_INPUT,
            font=Fonts.body()
        )
        self.url_entry.pack(fill="x")
        
        # URL validation message label
        self.url_error_label = ctk.CTkLabel(
            inner,
            text="",
            font=Fonts.small(),
            text_color=Colors.ERROR,
            anchor="w"
        )
        self.url_error_label.pack(fill="x", pady=(4, 0))
        
        # Bind focus events
        self.url_entry.bind("<FocusIn>", lambda e: self.url_entry.configure(
            border_color=Colors.PRIMARY_LIGHT
        ))
        self.url_entry.bind("<FocusOut>", self._on_url_focus_out)
        
        # Bind validation on text change
        self.job_url.trace_add("write", self._validate_comeet_url)
        
        # Keyboard shortcuts - return "break" to prevent double paste
        self.url_entry.bind('<Control-v>', self._handle_paste)
        self.url_entry.bind('<Control-V>', self._handle_paste)
        
    def _paste_url(self) -> None:
        """Paste URL from clipboard."""
        try:
            clipboard_text = self.root.clipboard_get()
            self.job_url.set(clipboard_text)
        except tk.TclError:
            pass
    
    def _handle_paste(self, event=None) -> str:
        """Handle Ctrl+V paste and prevent double paste."""
        self._paste_url()
        return "break"  # Prevent default paste behavior
    
    def _on_url_focus_out(self, event=None) -> None:
        """Handle URL entry focus out - validate and update border."""
        url = self.job_url.get().strip()
        if url and not is_valid_comeet_url(url):
            self.url_entry.configure(border_color=Colors.ERROR)
        else:
            self.url_entry.configure(border_color=Colors.BORDER_DEFAULT)
    
    def _validate_comeet_url(self, *args) -> None:
        """Validate URL and show/hide error message."""
        url = self.job_url.get().strip()
        
        if not url:
            # Empty URL - no error shown yet
            self.url_error_label.configure(text="")
            self.url_entry.configure(border_color=Colors.BORDER_DEFAULT)
        elif is_valid_comeet_url(url):
            # Valid Comeet URL
            self.url_error_label.configure(text="✓ Valid Comeet URL", text_color=Colors.SUCCESS)
            self.url_entry.configure(border_color=Colors.SUCCESS)
        else:
            # Invalid URL
            self.url_error_label.configure(
                text="⚠ URL must be a Comeet link (e.g., https://www.comeet.com/jobs/...)",
                text_color=Colors.ERROR
            )
            self.url_entry.configure(border_color=Colors.ERROR)
