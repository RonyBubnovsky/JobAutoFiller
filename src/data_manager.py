import json
import os
from tkinter import messagebox

from src.constants import DATA_FILE


def load_saved_data(form_data: dict) -> None:
    """Loads data from JSON file if it exists."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in data.items():
                    if k in form_data:
                        form_data[k].set(v)
        except Exception:
            pass


def save_current_data(form_data: dict) -> None:
    """Saves current inputs to JSON file."""
    data_to_save = {k: v.get() for k, v in form_data.items()}
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save settings: {e}")
