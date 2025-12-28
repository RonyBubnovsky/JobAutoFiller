# JobAutoFiller

A simple and efficient Python tool to automate filling out job application forms on **Comeet ATS platforms only**.

The tool saves your personal details locally and uses a graphical interface (GUI) to launch a browser, navigate to the job link, and auto-fill the fields.

> ⚠️ **Note:** This tool is specifically designed for Comeet-based job application pages. It will not work on other ATS platforms (Greenhouse, Lever, Workday, etc.).

## Features

- **GUI Interface:** Easy to use interface to input your details.
- **Auto-Save:** Remembers your details for the next time (saved locally).
- **Smart Form Filling:** Automatically detects First Name, Last Name, Email, Phone, LinkedIn, and Website fields.
- **Resume Upload:** Bypasses the system file dialog and uploads your CV directly.
- **Browser Control:** Opens the browser and keeps it open so you can review the application before submitting.

## Technologies

- **Python 3**
- **Tkinter** (For the User Interface)
- **Selenium** (For Browser Automation)
- **WebDriver Manager** (Auto-manages Chrome drivers)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/RonyBubnovsky/JobAutoFiller.git](https://github.com/RonyBubnovsky/JobAutoFiller.git)
    cd JobAutoFiller
    ```

2.  **Create a Virtual Environment (Optional but recommended):**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On Mac/Linux
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  Run the script:
    ```bash
    python main.py
    ```
2.  Fill in your details (Name, Email, Phone, etc.).
3.  Select your Resume (PDF/DOCX) from your computer.
4.  Paste the **Job URL** (e.g., a Comeet link).
5.  Click **"Open & Fill Form"**.
6.  The bot will open Chrome, go to the link, and fill in the data.
7.  **Review the form and click "Submit" manually.**

## Note

This tool uses `chromedriver`. It will automatically download the correct version for your browser. ensure you have Google Chrome installed.
