"""Theme configuration and constants for the GUI."""

import customtkinter as ctk

# Configure CustomTkinter appearance
def setup_theme():
    """Initialize the application theme."""
    ctk.set_appearance_mode("dark")  # "light", "dark", or "system"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


# Color constants
class Colors:
    """Color palette for the application."""
    
    # Primary colors
    PRIMARY = ("#3b82f6", "#2563eb")
    PRIMARY_HOVER = ("#2563eb", "#1d4ed8")
    PRIMARY_LIGHT = ("#60a5fa", "#3b82f6")
    
    # Success colors
    SUCCESS = ("#16a34a", "#22c55e")
    SUCCESS_LIGHT = ("#22c55e", "#16a34a")
    
    # Error colors
    ERROR = ("#dc2626", "#ef4444")
    ERROR_BG = ("#fee2e2", "#450a0a")
    
    # Neutral colors
    BORDER_DEFAULT = ("gray70", "gray30")
    BORDER_CARD = ("gray80", "gray25")
    
    TEXT_PRIMARY = ("gray20", "gray90")
    TEXT_SECONDARY = ("gray30", "gray70")
    TEXT_MUTED = ("gray50", "gray50")
    TEXT_HINT = ("gray60", "gray50")
    
    BG_CARD = ("gray95", "gray17")
    BG_INPUT = ("white", "gray20")
    BG_BUTTON_SECONDARY = ("gray85", "gray30")
    BG_BUTTON_SECONDARY_HOVER = ("gray75", "gray40")
    
    TRANSPARENT = "transparent"


# Font configurations
class Fonts:
    """Font configurations for the application."""
    
    FAMILY = "Segoe UI"
    
    @staticmethod
    def title():
        return ctk.CTkFont(family=Fonts.FAMILY, size=22, weight="bold")
    
    @staticmethod
    def subtitle():
        return ctk.CTkFont(family=Fonts.FAMILY, size=12)
    
    @staticmethod
    def header():
        return ctk.CTkFont(family=Fonts.FAMILY, size=16, weight="bold")
    
    @staticmethod
    def label():
        return ctk.CTkFont(family=Fonts.FAMILY, size=13, weight="bold")
    
    @staticmethod
    def body():
        return ctk.CTkFont(family=Fonts.FAMILY, size=13)
    
    @staticmethod
    def small():
        return ctk.CTkFont(family=Fonts.FAMILY, size=11)
    
    @staticmethod
    def hint():
        return ctk.CTkFont(family=Fonts.FAMILY, size=10)
    
    @staticmethod
    def button():
        return ctk.CTkFont(family=Fonts.FAMILY, size=15, weight="bold")
    
    @staticmethod
    def button_hover():
        return ctk.CTkFont(family=Fonts.FAMILY, size=16, weight="bold")
    
    @staticmethod
    def icon():
        return ctk.CTkFont(size=18)
    
    @staticmethod
    def icon_large():
        return ctk.CTkFont(size=24)
