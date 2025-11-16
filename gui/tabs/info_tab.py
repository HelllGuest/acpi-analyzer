"""Information Tab"""

import tkinter as tk
from tkinter import ttk



class InfoTab:
    """Information and help tab"""
    
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = ttk.Frame(parent)
        self.setup_tab()
    
    def setup_tab(self):
        """Setup the info tab"""
        # Title
        title = ttk.Label(self.frame, text="Acpi Analyzer v1.0 - Information & Help")
        title.pack()
        
        # Create notebook for info sections
        info_notebook = ttk.Notebook(self.frame)
        info_notebook.pack(fill=tk.BOTH, expand=True)
        
        # About tab
        about_frame = ttk.Frame(info_notebook)
        info_notebook.add(about_frame, text="About")
        self.create_about_section(about_frame)
        
        # Quick Start tab
        quickstart_frame = ttk.Frame(info_notebook)
        info_notebook.add(quickstart_frame, text="Quick Start")
        self.create_quickstart_section(quickstart_frame)
        
        # Patches tab
        patches_frame = ttk.Frame(info_notebook)
        info_notebook.add(patches_frame, text="Patch Guide")
        self.create_patches_section(patches_frame)
    
    def create_about_section(self, parent):
        """Create about section"""
        text = tk.Text(parent, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        
        content = """Acpi Analyzer v1.0

A comprehensive ACPI analysis and SSDT patching tool for Hackintosh 
development and system administration.

Author: Anoop Kumar
License: MIT License
Source: https://github.com/HelllGuest/acpi-analyzer

Features:
- 74 SSDT patches with 193 templates
- Automatic hardware detection from DSDT analysis
- Manual patch editor with complete template library
- Device database with 50+ device IDs
- Cross-platform support (Windows, Linux, macOS)
- Zero dependencies (only Python + tkinter)
- Clean, modular, and extensible architecture

Application Tabs:
- ACPI Analysis - Device discovery, tree view, JSON export
- Auto-Patch - Main patch generation with smart recommendations
- Manual Patches - Template editor with 193 templates
- Information - This help section

Architecture:
- Core Module - Patch management, ACPI parsing, hardware detection
- GUI Module - Main window and tab implementations
- Generators - 25 working SSDT generators
- Data Module - Device and hardware databases
- Templates - 193 official SSDT templates

Built with Python & Tkinter
Uses native system styling for maximum compatibility

Version: 1.0
License: MIT License
"""
        text.insert('1.0', content)
        text.config(state=tk.DISABLED)
    
    def create_quickstart_section(self, parent):
        """Create quick start section"""
        text = tk.Text(parent, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        
        content = """Quick Start Guide

Getting Started:

Step 1: Load DSDT File
- Go to File -> Open DSDT/ACPI File
- Select your decompiled DSDT.dsl file
- The tool will parse and analyze the file
- To close: File -> Close DSDT/ACPI File

Step 2: Set Output Directory
- Go to File -> Set Output Directory
- Choose where to save generated SSDTs
- This is where .dsl files will be created
- To clear: File -> Clear Output Directory

Step 3: Analyze Hardware (Auto-Patch Tab)
- Switch to the Auto-Patch tab
- Click "Analyze Hardware" button
- Reviews DSDT content and detects devices
- Shows platform type (Desktop/Laptop)

Step 4: Select Patches
- Option A: Click "Auto-Select Patches" (recommended)
  Automatically selects essential and recommended patches
- Option B: Manually check desired patches from the list
  Browse 74 patches in 12 categories

Step 5: Generate SSDTs
- Click "Generate Selected" for checked patches only
- Or click "Generate All" to generate all 74 patches
- Watch progress bar for completion
- Files will be created in your output directory

Step 6: Deploy to macOS
- Copy generated .dsl files to EFI/OC/ACPI/
- Compile to .aml using MaciASL or iasl (if needed)
- Update config.plist ACPI section
- Reboot and test your system

Additional Features:
- ACPI Analysis Tab: View device tree, export to JSON
- Manual Patches Tab: Edit 193 templates directly
- Tools Menu: Reset patches, refresh all tabs
- Help Menu: Quick start, documentation, about

Tips:
- Always start with essential patches (EC, PLUG, AWAC)
- Desktop systems need PMC for 300+ series chipsets
- Laptops need PNLF for backlight control
- Use Manual Patches tab for custom modifications
- Check ACPI Analysis tab for device information
- Export analysis to JSON for documentation
"""
        text.insert('1.0', content)
        text.config(state=tk.DISABLED)
    
    def create_patches_section(self, parent):
        """Create patches guide section"""
        text = tk.Text(parent, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        
        content = """Patch Guide

Essential Patches (REQUIRED):

SSDT-EC - Fake Embedded Controller
- Required for Catalina+ to boot
- Creates fake EC device
- Priority: CRITICAL

SSDT-PLUG - CPU Power Management
- Enables XCPM on Haswell and newer
- Required for proper CPU power management
- Priority: CRITICAL

SSDT-AWAC - System Clock Fix
- Required for 300+ series chipsets
- Forces RTC to be enabled
- Priority: HIGH

Hardware Patches:

SSDT-HPET - IRQ Conflict Resolution
- Fixes audio and USB issues
- Resolves IRQ conflicts
- Priority: HIGH

SSDT-PMC - NVRAM Support
- Required for 300+ series chipsets
- Enables native NVRAM
- Priority: HIGH

SSDT-SBUS - System Management Bus
- Adds SMBus support
- Recommended for all systems
- Priority: MEDIUM

Laptop Patches:

SSDT-PNLF - Backlight Control
- REQUIRED for laptop backlight
- Enables brightness control
- Priority: CRITICAL (Laptops)

SSDT-ALS0 - Ambient Light Sensor
- Adds fake ALS device
- Optional enhancement
- Priority: MEDIUM

SSDT-GPI0 - GPIO Controller
- Required for I2C trackpad support
- Enables GPIO devices
- Priority: HIGH (Laptops)

USB Patches:

SSDT-USBX - USB Power Properties
- Sets proper USB power values
- Recommended for all systems
- Priority: HIGH

SSDT-USB-Reset - Reset USB Hubs
- Helps with USB detection issues
- Optional fix
- Priority: MEDIUM

Usage Recommendations:
- Desktop: EC, PLUG, AWAC, HPET, PMC, SBUS, USBX
- Laptop: EC, PLUG, AWAC, HPET, PNLF, GPI0, USBX
- HEDT: Add UNC, RTC0-RANGE patches
"""
        text.insert('1.0', content)
        text.config(state=tk.DISABLED)
    
    def refresh(self):
        """Refresh the tab"""
        return
