#!/usr/bin/env python3
"""
JobAutoFiller - Automate job application form filling on Comeet platforms.
"""

import customtkinter as ctk
from src.gui import AutoApplierGUI


def main():
    """Entry point for the application."""
    root = ctk.CTk()
    AutoApplierGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()