"""Status bar component."""

import customtkinter as ctk
from src.gui.theme import Colors, Fonts


class StatusBar(ctk.CTkFrame):
    """Modern status bar with animated progress."""
    
    def __init__(self, master):
        super().__init__(
            master,
            height=60,
            corner_radius=12,
            fg_color=Colors.BG_CARD
        )
        self.pack_propagate(False)
        
        inner = ctk.CTkFrame(self, fg_color=Colors.TRANSPARENT)
        inner.pack(fill="both", expand=True, padx=16, pady=12)
        
        self.status_icon = ctk.CTkLabel(
            inner,
            text="⚡",
            font=Fonts.icon()
        )
        self.status_icon.pack(side="left")
        
        self.status_text = ctk.CTkLabel(
            inner,
            text="Ready to fill applications",
            font=Fonts.body(),
            text_color=("gray40", "gray60")
        )
        self.status_text.pack(side="left", padx=(8, 0))
        
        self.progress = ctk.CTkProgressBar(
            inner,
            width=100,
            height=8,
            corner_radius=4,
            progress_color=Colors.PRIMARY_LIGHT
        )
        self.progress.pack(side="right")
        self.progress.set(0)
        
    def set_status(self, text: str, icon: str = "⚡", progress: float = 0):
        """Update status bar state."""
        self.status_text.configure(text=text)
        self.status_icon.configure(text=icon)
        self.progress.set(progress)
        
    def set_loading(self, text: str = "Processing..."):
        """Show loading state."""
        self.status_text.configure(text=text)
        self.status_icon.configure(text="🔄")
        # Animate progress
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        
    def set_success(self, text: str = "Completed!"):
        """Show success state."""
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(1)
        self.status_text.configure(text=text)
        self.status_icon.configure(text="✅")
        
    def set_error(self, text: str = "Error occurred"):
        """Show error state."""
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(0)
        self.status_text.configure(text=text)
        self.status_icon.configure(text="❌")
        
    def reset(self):
        """Reset to default state."""
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(0)
        self.status_text.configure(text="Ready to fill applications")
        self.status_icon.configure(text="⚡")
