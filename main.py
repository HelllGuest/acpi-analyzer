#!/usr/bin/env python3
"""
Acpi Analyzer - Main Entry Point
A comprehensive ACPI analysis and patching tool
"""

import sys
import tkinter as tk
from tkinter import messagebox

def main():
    """Main application entry point"""
    try:
        from gui.main_window import AcpiAnalyzerApp
        
        root = tk.Tk()
        app = AcpiAnalyzerApp(root)
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror(
            "Startup Error",
            f"Failed to start Acpi Analyzer:\n{str(e)}\n\n"
            f"Please ensure all files are present and Python 3.6+ is installed."
        )
        raise

if __name__ == "__main__":
    main()
