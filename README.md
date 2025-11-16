# Acpi Analyzer

A comprehensive ACPI analysis and SSDT patching tool for Hackintosh development and system administration.

**Version:** 1.0  
**Author:** Anoop Kumar  
**License:** MIT  

## Overview

Acpi Analyzer is a self-contained Python application that provides everything you need for ACPI table analysis and SSDT patch generation. With 75 patches, 193 templates, and automatic hardware detection, it's a comprehensive ACPI tooling solution.

## Features

- **75 SSDT Patches** - Complete library covering all common use cases
- **193 Templates** - Official templates from Dortania and community sources
- **DSDT-Specific Patch Generation** - Automatically detects device paths from your DSDT
- **Smart Device Detection** - Finds PCI root, LPC bridge, GPU, CPU, USB, SMBus, and more
- **Intelligent Fallbacks** - Uses generic paths with warnings when devices not detected
- **Hardware Analysis** - Comprehensive DSDT analysis with detected device paths
- **Manual Editor** - Full-featured template editor with 193 templates
- **Device Database** - 33 device IDs with categorization
- **Cross-Platform** - Works on Windows, Linux, and macOS
- **Zero Dependencies** - Only requires Python 3.6+ with tkinter (included)
- **Clean Interface** - Simple 4-tab GUI with quick-access buttons
- **One-Click Reset** - Single button to reset all data and start fresh

## Quick Start

### Installation

No installation required! Just run:

```bash
python main.py
```

### Requirements

- Python 3.6 or higher (with tkinter)
- No additional dependencies

### 5-Minute Workflow

1. **Launch Application**
   ```bash
   python main.py
   ```

2. **Load DSDT File**
   - Click "Open DSDT" button (or File -> Open DSDT/ACPI File)
   - Select your decompiled DSDT.dsl file

3. **Set Output Directory**
   - Click "Set Output" button (or File -> Set Output Directory)
   - Choose where to save generated patches

4. **Analyze Hardware**
   - Go to Auto-Patch tab
   - Click "Analyze Hardware"
   - Review detected device paths and compatibility

5. **Select Patches**
   - Click "Auto-Select Patches" (recommended)
   - Or manually check desired patches

6. **Generate SSDTs**
   - Click "Generate Selected"
   - Patches will use detected paths from your DSDT
   - Wait for completion message

7. **Review Generated Files**
   - Open generated .dsl files
   - Check header comments for detected paths and warnings
   - Verify compatibility status

8. **Deploy to macOS**
   - Copy generated .dsl files to EFI/OC/ACPI/
   - Compile to .aml if needed using MaciASL or iasl
   - Update config.plist ACPI section
   - Reboot and test

**Need to start over?** Click the "Reset" button to clear everything!

## Application Interface

**Quick Access Buttons:** Open DSDT, Set Output, Reset

**Tab 1: ACPI Analysis**
- Device discovery and tree view
- JSON export and statistics

**Tab 2: Auto-Patch (Main Feature)**
- DSDT-specific patch generation with device path detection
- 74 patches in 12 categories
- Smart fallbacks with warnings
- Batch generation with progress tracking

**Tab 3: Manual Patches**
- 193 SSDT templates
- Code editor with undo/redo
- Load, edit, and save patches

**Tab 4: Information**
- Patch guides and documentation
- Built-in help

## What Makes This Tool Special

**DSDT-Specific Patch Generation** - Unlike generic tools, Acpi Analyzer detects actual device paths from your DSDT.

**Example:** If your DSDT uses `_SB.PC00.LPC0` instead of `_SB.PCI0.LPCB`:

Generic Tool:
```c
External (_SB_.PCI0.LPCB, DeviceObj)  // Won't work!
```

Acpi Analyzer:
```c
/* Device Path: _SB.PC00.LPC0 (detected from DSDT) */
External (_SB_.PC00.LPC0_, DeviceObj)  // Uses YOUR path!
```

**Benefits:** No manual editing, patches work immediately, clear warnings when needed.

## Complete Patch Library

### Essential (3 patches) - REQUIRED
- **SSDT-EC** - Fake Embedded Controller (Required for Catalina+)
- **SSDT-PLUG** - CPU Power Management (Required for XCPM)
- **SSDT-AWAC** - System Clock Fix (Required for 300+ series)

### Hardware (15 patches)
- SSDT-HPET - IRQ Conflict Resolution
- SSDT-PMC - NVRAM Support (300+ series)
- SSDT-SBUS - System Management Bus
- SSDT-MCHC - Memory Controller
- SSDT-IMEI - Management Engine Interface
- SSDT-DMAC - DMA Controller
- SSDT-MEM2 - Memory Controller 2
- SSDT-PPMC - Platform Power Management
- SSDT-HPET_RTC_TIMR-fix - IRQ Fix
- SSDT-SMBU - SMBus Alternative
- SSDT-RTC0-NoFlags - RTC without Flags
- SSDT-IPIC - Interrupt Controller
- SSDT-SBUS-MCHC - Combined patch
- SSDT-PMCR - PMC Alternative

### Laptop (6 patches)
- SSDT-PNLF - Backlight Control (REQUIRED for laptops)
- SSDT-ALS0 - Ambient Light Sensor
- SSDT-GPI0 - GPIO Controller (I2C trackpad support)
- SSDT-XOSI - OS Interface patches
- SSDT-PRW - Instant Wake Fix
- SSDT-Battery - Battery Status Reporting

### USB (3 patches)
- SSDT-USBX - USB Power Properties
- SSDT-USB-Reset - Reset USB Hubs
- SSDT-EHCx_OFF - Disable EHC Controllers

### Advanced (14 patches)
- SSDT-XOSI - OS Interface patches
- SSDT-GPU-DISABLE - Disable discrete GPU
- SSDT-GPU-SPOOF - Spoof GPU device ID
- SSDT-dGPU-Off - Alternative GPU disable
- SSDT-NoHybGfx - Disable hybrid graphics
- SSDT-RHUB - USB Hub Reset
- SSDT-RHUB-prebuilt - USB Hub Reset alternative
- SSDT-UNC - Uncore Bridge (HEDT)
- SSDT-RTC0-RANGE - RTC Range (HEDT)
- SSDT-CPUR - CPU Renaming
- SSDT-IMEI - Intel Management Engine
- SSDT-EC-USBX-DESKTOP - Combined EC+USBX Desktop
- SSDT-EC-USBX-LAPTOP - Combined EC+USBX Laptop
- SSDT-PLUG-DRTNIA - Alternative PLUG

### Battery (5 patches)
- SSDT-BATS - Battery Status Generic
- SSDT-BATT - Battery Status Alternative
- SSDT-OCBAT0-TP - ThinkPad Battery
- SSDT-OCBAT0-HP - HP Battery
- SSDT-OCBAT0-ASUS - ASUS Battery

### Trackpad (5 patches)
- SSDT-I2C0-TPXX - I2C Trackpad Generic
- SSDT-I2C1-TPXX - I2C Trackpad Alternative
- SSDT-ThinkPad_ClickPad - ThinkPad ClickPad
- SSDT-OCI2C-TPXX - OpenCore I2C Generic
- SSDT-ThinkPad_TrackPad - ThinkPad TrackPad

### Display (5 patches)
- SSDT-PNLF-CFL - Coffee Lake Backlight
- SSDT-PNLF-SKL_KBL - Skylake/Kaby Lake Backlight
- SSDT-PNLF-Haswell_Broadwell - Haswell/Broadwell Backlight
- SSDT-PNLF-SNB_IVY - Sandy Bridge/Ivy Bridge Backlight
- SSDT-PNLF-ACPI - ACPI Method Backlight

### Graphics (4 patches)
- SSDT-DGPU - Disable Discrete GPU
- SSDT-NDGP_OFF - Disable NVIDIA GPU
- SSDT-RX580 - AMD RX 580 Support
- SSDT-NDGP_PS3 - NVIDIA GPU Power State

### Power (8 patches)
- SSDT-GPRW - Instant Wake Fix
- SSDT-PTSWAKTTS - Sleep/Wake Fix
- SSDT-LIDpatch - Lid Wake Fix
- SSDT-UPRW - USB Power Wake Fix
- SSDT-XPRW - Extended Power Wake
- SSDT-DeepIdle - Deep Idle Power
- SSDT-PWRB - Power Button Device
- SSDT-SLPB - Sleep Button Device

### Input (4 patches)
- SSDT-RMCF-PS2Map-AtoZ - PS2 Keyboard Mapping
- SSDT-BKeyQ11Q12 - Brightness Keys
- SSDT-RMCF-PS2Map-dell - PS2 Keyboard Dell
- SSDT-RMCF-PS2Map-Lenovo - PS2 Keyboard Lenovo

### Compatibility (2 patches)
- SSDT-OC-XOSI - OpenCore XOSI
- SSDT-Darwin - Darwin OS Detection

### Quick Reference

**Desktop (Coffee Lake+):**
- Required: SSDT-EC-USBX, SSDT-PLUG, SSDT-AWAC, SSDT-PMC
- Recommended: SSDT-HPET, SSDT-SBUS, SSDT-GPRW

**Laptop (Coffee Lake+):**
- Required: SSDT-EC-USBX, SSDT-PLUG, SSDT-AWAC, SSDT-PNLF, SSDT-GPI0
- Recommended: SSDT-HPET, SSDT-ALS0, SSDT-GPRW, Battery/Trackpad patches

**HEDT (Haswell-E+):**
- Required: SSDT-EC-USBX, SSDT-PLUG, SSDT-RTC0-RANGE, SSDT-UNC, SSDT-HPET

**Notes:**
- Use "Analyze Hardware" in Auto-Patch tab for automatic detection
- "Auto-Select Patches" chooses appropriate patches based on detected platform
- Older platforms (Sandy/Ivy Bridge) require CPU-PM in Post-Install
- IRQ SSDT only needed for older laptops with IRQ conflicts

Reference: [Dortania ACPI Guide](https://dortania.github.io/Getting-Started-With-ACPI/)

## Menu Reference

### File Menu
- **Open DSDT/ACPI File** - Load your DSDT.dsl file
- **Set Output Directory** - Choose where to save generated patches
- **Reset** - Clear all data (DSDT file, output directory, patches, analysis)
- **Exit** - Close the application

### Tools Menu
- **Reset All Patches** - Uncheck all selected patches
- **Refresh All** - Refresh all tabs

### Help Menu
- **About** - Application information and credits

## Project Structure

```
acpi-analyzer/
├── main.py                    # Application entry point
├── README.md                  # This file
├── core/                      # Core functionality
│   ├── __init__.py
│   ├── patch_info.py         # 74 patches management
│   ├── acpi_parser.py        # DSDT/SSDT parsing with device detection
│   ├── dsdt_context.py       # DSDT context manager for detected paths
│   ├── hardware_detector.py  # Hardware detection
│   └── generators/           # SSDT generators
│       ├── __init__.py
│       ├── essential_generators.py    # EC, PLUG, AWAC (DSDT-aware)
│       ├── hardware_generators.py     # HPET, PMC, SBUS (DSDT-aware)
│       ├── laptop_generators.py       # PNLF, ALS0, GPI0 (DSDT-aware)
│       ├── usb_generators.py          # USBX, USB-Reset (DSDT-aware)
│       ├── advanced_generators.py     # Template-based generators
│       └── templates/        # 193 SSDT templates
├── gui/                       # User interface
│   ├── __init__.py
│   ├── main_window.py        # Main window with quick-access buttons
│   └── tabs/                 # Tab implementations
│       ├── __init__.py
│       ├── analysis_tab.py   # ACPI Analysis
│       ├── autopatch_tab.py  # Auto-Patch with DSDT detection
│       ├── manual_tab.py     # Manual Editor
│       └── info_tab.py       # Information
└── data/                      # Data files
    ├── __init__.py
    └── device_database.py    # 50+ device IDs
```

## Technical Details

**System Requirements:**
- Python 3.6+ (with tkinter)
- Windows 7+, Linux, macOS 10.12+
- 512MB RAM, 50MB storage

**Code Quality:**
- No external dependencies (Python standard library only)
- Clean, modular architecture
- Cross-platform compatibility

### Hardware Detection & DSDT Analysis

Analyzes DSDT file content to detect device paths:
- **PCI Root** (PCI0, PC00, PCIO, PCI1, PCIE)
- **LPC Bridge** (LPCB, LPC0, LPC, SBRG)
- **GPU** (GFX0, IGPU, VID, VGA)
- **CPU** (_PR.CPU0, _SB.PR00, _SB.CP00)
- **USB** (XHC, XHCI, XHC1, EHC1, EHC2)
- **SMBus** (SBUS, SMBU, SMBS)
- **EC, Battery, HPET, GPIO** and more

Generated patches use detected paths or fall back to generic paths with warnings.

## Troubleshooting

**"No module named 'tkinter'"**
```bash
Ubuntu/Debian: sudo apt-get install python3-tk
CentOS/RHEL:   sudo yum install tkinter
macOS:         brew install python-tk
Windows:       Reinstall Python with "tcl/tk and IDLE" checked
```

**"Please load a DSDT file first"**
- Click "Open DSDT" button or File -> Open DSDT/ACPI File
- Ensure file is .dsl format (decompiled)

**"No patches generated"**
- Set output directory first (click "Set Output" button)
- Check write permissions to output folder
- Ensure at least one patch is selected

## Acknowledgments

- **Dortania** - ACPI guides and templates
- **OpenCore Community** - SSDT patches and documentation
- **Acidanthera** - OpenCore and related tools

## Support

For help:
1. Review this README.md file for complete documentation
2. Check the Information tab in the application for patch guides
4. Visit: https://github.com/HelllGuest/acpi-analyzer

## Project Statistics

- **Total Files**: 215 files
- **Python Code**: 21 files (~3,000 lines)
- **SSDT Templates**: 193 files
- **Patches Available**: 75 SSDT patches
- **Categories**: 12 patch categories
- **DSDT-Aware Generators**: 11 generators with device path detection
- **Template-Based Generators**: 14+ generators
- **Device Database**: 33 device IDs
- **Detectable Device Types**: 10+ (PCI root, LPC, GPU, CPU, USB, etc.)

## Changelog

### Version 1.0 (Current)
- **DSDT-Specific Patch Generation** - Automatically detects and uses actual device paths
- **Smart Device Detection** - Finds 10+ device types from DSDT
- **Intelligent Fallbacks** - Uses generic paths with warnings when needed
- **Enhanced Hardware Analysis** - Shows all detected device paths
- **Quick Access Buttons** - Open DSDT, Set Output, Reset buttons
- **One-Click Reset** - Single button to clear all data
- **Simplified Menu** - Streamlined File menu with Reset option
- **Professional Output** - Generated patches include metadata and compatibility status
- **11 DSDT-Aware Generators** - Essential, Hardware, Laptop, and USB patches
- **Clean Architecture** - Modular design with DSDT context manager

---
