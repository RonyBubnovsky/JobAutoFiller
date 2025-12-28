#!/usr/bin/env python3
"""
JobAutoFiller - Automate job application form filling on Comeet platforms.
"""

import tkinter as tk
from src.gui import AutoApplierGUI


def main():
    """Entry point for the application."""
    root = tk.Tk()
    AutoApplierGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()