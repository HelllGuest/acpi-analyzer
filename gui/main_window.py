"""Main application window"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from core.patch_info import PatchManager
from core.acpi_parser import ACPIParser
from core.hardware_detector import HardwareDetector

from gui.tabs.analysis_tab import AnalysisTab
from gui.tabs.autopatch_tab import AutoPatchTab
from gui.tabs.manual_tab import ManualTab
from gui.tabs.info_tab import InfoTab


class AcpiAnalyzerApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Acpi Analyzer v1.0")
        
        # Initialize managers
        self.patch_manager = PatchManager()
        self.acpi_parser = ACPIParser()
        self.hardware_detector = HardwareDetector(self.acpi_parser)
        
        # Application state
        self.current_file = None
        self.output_directory = None
        self.acpi_entries = []
        self.dsdt_context = None
        
        # Setup UI
        self.create_menu()
        self.create_main_ui()
        self.create_status_bar()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open DSDT/ACPI File", command=self.open_file)
        file_menu.add_command(label="Set Output Directory", command=self.set_output_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Reset", command=self.reset_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Reset All Patches", command=self.reset_patches)
        tools_menu.add_command(label="Refresh All", command=self.refresh_all)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_ui(self):
        """Create main UI"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top button bar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Open DSDT", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Set Output", command=self.set_output_directory).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Reset", command=self.reset_all).pack(side=tk.LEFT, padx=2)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.analysis_tab = AnalysisTab(self.notebook, self)
        self.autopatch_tab = AutoPatchTab(self.notebook, self)
        self.manual_tab = ManualTab(self.notebook, self)
        self.info_tab = InfoTab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.analysis_tab.frame, text="ACPI Analysis")
        self.notebook.add(self.autopatch_tab.frame, text="Auto-Patch")
        self.notebook.add(self.manual_tab.frame, text="Manual Patches")
        self.notebook.add(self.info_tab.frame, text="Information")
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress = ttk.Progressbar(self.status_frame, mode='determinate')
        self.progress.pack(side=tk.RIGHT)
    
    def open_file(self):
        """Open DSDT or ACPI folder"""
        filepath = filedialog.askopenfilename(
            title="Select DSDT File",
            filetypes=[("DSL Files", "*.dsl"), ("All Files", "*.*")]
        )
        
        if filepath:
            self.current_file = Path(filepath)
            self.update_status(f"Loaded: {self.current_file.name}")
            
            # Parse file
            if self.acpi_parser.parse_file(filepath):
                self.acpi_entries = self.acpi_parser.get_all_devices()
                messagebox.showinfo("Success", 
                    f"Loaded {len(self.acpi_entries)} devices from {self.current_file.name}")
                self.refresh_all()
            else:
                messagebox.showerror("Error", "Failed to parse ACPI file")
    
    def set_output_directory(self):
        """Set output directory for generated files"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory = Path(directory)
            self.update_status(f"Output: {self.output_directory}")
            messagebox.showinfo("Success", f"Output directory set to:\n{self.output_directory}")
    
    def reset_all(self):
        """Reset everything - DSDT file, output directory, patches, and context"""
        # Reset DSDT file
        self.current_file = None
        self.acpi_entries = []
        self.acpi_parser = ACPIParser()
        self.dsdt_context = None
        
        # Reset output directory
        self.output_directory = None
        
        # Reset patches
        self.patch_manager.reset_all()
        
        # Refresh UI
        self.refresh_all()
        
        self.update_status("Reset complete - all data cleared")
        messagebox.showinfo("Reset Complete", "All data has been reset:\n\n- DSDT file closed\n- Output directory cleared\n- Patch selections cleared\n- Analysis data cleared")
    
    def reset_patches(self):
        """Reset all patch selections"""
        self.patch_manager.reset_all()
        self.refresh_all()
        self.update_status("All patches reset")
    
    def refresh_all(self):
        """Refresh all tabs"""
        self.analysis_tab.refresh()
        self.autopatch_tab.refresh()
        self.manual_tab.refresh()
        self.info_tab.refresh()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress['value'] = value
        self.root.update_idletasks()
    
    def show_about(self):
        """Show about dialog"""
        about = """Acpi Analyzer v1.0

A comprehensive ACPI analysis and SSDT patching tool
for Hackintosh development and system administration.

Author: Anoop Kumar
License: MIT License
Source: https://github.com/HelllGuest/acpi-analyzer

Features:
- 74 SSDT patches with 193 templates
- DSDT-specific patch generation
- Automatic device path detection
- Manual patch editor with template library
- Device database with 33 device IDs
- Cross-platform support (Windows/Linux/macOS)

Built with Python & Tkinter
Clean, modular, and extensible architecture"""
        
        messagebox.showinfo("About Acpi Analyzer", about)
