"""Auto-Patch Tab - Main feature"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from core.generators import EssentialGenerators, HardwareGenerators, LaptopGenerators, USBGenerators, AdvancedGenerators


class AutoPatchTab:
    """Automatic patch generation tab"""
    
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = ttk.Frame(parent)
        self.patch_vars = {}
        self.setup_tab()
    
    def setup_tab(self):
        """Setup the auto-patch tab"""
        # Title
        title = ttk.Label(self.frame, text="Auto-Patch - Automatic SSDT Generation")
        title.pack()
        
        # Control buttons
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Analyze Hardware", 
                  command=self.analyze_hardware).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Auto-Select Patches", 
                  command=self.auto_select).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Generate Selected", 
                  command=self.generate_selected).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Generate All", 
                  command=self.generate_all).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Clear Selection", 
                  command=self.clear_selection).pack(side=tk.LEFT)
        
        # Hardware info
        hw_frame = ttk.LabelFrame(self.frame, text="Hardware Detection")
        hw_frame.pack(fill=tk.X)
        
        self.hw_text = tk.Text(hw_frame, height=4, wrap=tk.WORD)
        self.hw_text.pack(fill=tk.BOTH, expand=True)
        self.hw_text.insert('1.0', "Load a DSDT file first (File -> Open DSDT/ACPI Folder)\n"
                                   "Then click 'Analyze Hardware' to detect system configuration from DSDT")
        
        # Patch list
        patch_frame = ttk.LabelFrame(self.frame, text="Available Patches")
        patch_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(patch_frame)
        scrollbar = ttk.Scrollbar(patch_frame, orient="vertical", command=canvas.yview)
        self.patch_list_frame = ttk.Frame(canvas)
        
        self.patch_list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.patch_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate patches
        self.populate_patches()
    
    def populate_patches(self):
        """Populate patch list"""
        # Clear existing
        for widget in self.patch_list_frame.winfo_children():
            widget.destroy()
        
        self.patch_vars = {}
        
        # Group by category
        categories = {}
        for patch in self.main_app.patch_manager.patches:
            if patch.category not in categories:
                categories[patch.category] = []
            categories[patch.category].append(patch)
        
        # Create checkboxes by category
        row = 0
        for category, patches in categories.items():
            # Category header
            cat_label = ttk.Label(self.patch_list_frame, 
                                 text=f"-- {category} --")
            cat_label.grid(row=row, column=0, columnspan=4, sticky=tk.W)
            row += 1
            
            # Patches in category
            for patch in patches:
                var = tk.BooleanVar(value=patch.checked)
                self.patch_vars[patch.name] = var
                
                # Checkbox
                cb = ttk.Checkbutton(self.patch_list_frame, variable=var,
                                    command=lambda p=patch, v=var: self.on_patch_toggle(p, v))
                cb.grid(row=row, column=0, sticky=tk.W)
                
                # Name
                name_label = ttk.Label(self.patch_list_frame, text=patch.name)
                name_label.grid(row=row, column=1, sticky=tk.W)
                
                # Description
                desc_label = ttk.Label(self.patch_list_frame, text=patch.description)
                desc_label.grid(row=row, column=2, sticky=tk.W)
                
                # Priority
                priority_label = ttk.Label(self.patch_list_frame, 
                                          text=f"[{patch.priority.upper()}]")
                priority_label.grid(row=row, column=3, sticky=tk.W)
                
                row += 1
    
    def on_patch_toggle(self, patch, var):
        """Handle patch checkbox toggle"""
        patch.checked = var.get()
    
    def analyze_hardware(self):
        """Analyze hardware and recommend patches"""
        # Check if DSDT is loaded
        if not self.main_app.current_file and not self.main_app.acpi_entries:
            messagebox.showwarning(
                "No DSDT Loaded",
                "Please load a DSDT file first:\n\n"
                "File -> Open DSDT/ACPI Folder\n\n"
                "The hardware detection will analyze your DSDT file to determine:\n"
                "- CPU type and generation\n"
                "- Platform type (Desktop/Laptop)\n"
                "- Chipset series\n"
                "- Required patches"
            )
            return
        
        self.main_app.update_status("Analyzing DSDT file...")
        
        # Create and analyze DSDT context
        from core.dsdt_context import DSDTContext
        self.main_app.dsdt_context = DSDTContext(self.main_app.acpi_parser)
        self.main_app.dsdt_context.analyze()
        
        # Get detected paths
        paths = self.main_app.dsdt_context.get_detection_summary()
        
        # Detect hardware from DSDT
        hw_info = self.main_app.hardware_detector.detect()
        
        # Analyze DSDT for additional info
        device_count = len(self.main_app.acpi_entries)
        has_ec = any('EC' in d.get('name', '') for d in self.main_app.acpi_entries)
        has_battery = any('BAT' in d.get('name', '') for d in self.main_app.acpi_entries)
        
        # Determine platform from DSDT
        if has_battery:
            platform = "Laptop"
        else:
            platform = hw_info.get('platform', 'Desktop')
        
        # Display results
        info_text = f"""Hardware Detection Results:

Source: {self.main_app.current_file.name if self.main_app.current_file else 'Loaded ACPI'}
Devices Found: {device_count}

CPU: {hw_info.get('cpu', 'Unknown')}
Platform: {platform}
Chipset: {hw_info.get('chipset', 'Unknown')}

Detected Device Paths:
  PCI Root: {paths['PCI Root']}
  LPC Bridge: {paths['LPC Bridge']}
  GPU Device: {paths['GPU Device']}
  CPU Path: {paths['CPU Path']}
  USB Controller: {paths['USB Controller']}
  SMBus: {paths['SMBus']}
  EC Device: {paths['EC Device']}
  Battery: {paths['Battery Device']}
  HPET: {paths['HPET Device']}
  GPIO: {paths['GPIO Device']}

Recommended Patches: {len(hw_info.get('recommended_patches', []))}

Note: Patches will use detected paths when available.
Generic paths will be used with warnings if devices not found.
"""
        
        self.hw_text.delete('1.0', tk.END)
        self.hw_text.insert('1.0', info_text)
        
        self.main_app.update_status("Hardware analysis complete")
        messagebox.showinfo("Analysis Complete", 
                          f"Analyzed: {self.main_app.current_file.name if self.main_app.current_file else 'ACPI'}\n"
                          f"Platform: {platform}\n"
                          f"Devices: {device_count}\n"
                          f"Detected Paths: {sum(1 for v in paths.values() if v != 'Not found')}/10\n"
                          f"Recommended: {len(hw_info.get('recommended_patches', []))} patches")
    
    def auto_select(self):
        """Automatically select recommended patches"""
        # Select essential patches
        essential_patches = ['SSDT-EC', 'SSDT-PLUG']
        
        for patch in self.main_app.patch_manager.patches:
            if patch.name in essential_patches or patch.priority == 'critical':
                patch.checked = True
                patch.recommended = True
                if patch.name in self.patch_vars:
                    self.patch_vars[patch.name].set(True)
        
        self.main_app.update_status("Auto-selected essential patches")
        messagebox.showinfo("Auto-Select", "Selected essential and critical patches")
    
    def generate_selected(self):
        """Generate selected patches"""
        if not self.main_app.output_directory:
            messagebox.showwarning("No Output Directory", 
                                 "Please set output directory first (File -> Set Output Directory)")
            return
        
        selected = self.main_app.patch_manager.get_checked_patches()
        if not selected:
            messagebox.showwarning("No Selection", "Please select patches to generate")
            return
        
        self.generate_patches(selected)
    
    def generate_all(self):
        """Generate all patches"""
        if not self.main_app.output_directory:
            messagebox.showwarning("No Output Directory", 
                                 "Please set output directory first")
            return
        
        self.generate_patches(self.main_app.patch_manager.patches)
    
    def generate_patches(self, patches):
        """Generate SSDT files"""
        self.main_app.update_status("Generating patches...")
        generated = []
        failed = []
        
        total = len(patches)
        for i, patch in enumerate(patches):
            self.main_app.update_progress((i + 1) / total * 100)
            
            output_file = self.main_app.output_directory / f"{patch.name}.dsl"
            
            try:
                success = self.generate_single_patch(patch.name, output_file)
                if success:
                    generated.append(patch.name)
                    patch.generated = True
                else:
                    failed.append(patch.name)
            except Exception as e:
                failed.append(f"{patch.name} ({str(e)})")
        
        self.main_app.update_progress(0)
        
        # Show results
        message = f"Generated {len(generated)} patches"
        if failed:
            message += f"\nFailed: {len(failed)}"
        
        self.main_app.update_status(message)
        messagebox.showinfo("Generation Complete", 
                          f"Successfully generated: {len(generated)}\n"
                          f"Failed: {len(failed)}\n\n"
                          f"Output: {self.main_app.output_directory}")
    
    def generate_single_patch(self, patch_name, output_path):
        """Generate a single patch file"""
        # Get DSDT context if available
        dsdt_context = getattr(self.main_app, 'dsdt_context', None)
        
        generators = {
            'SSDT-EC': EssentialGenerators.generate_ec,
            'SSDT-PLUG': EssentialGenerators.generate_plug,
            'SSDT-AWAC': EssentialGenerators.generate_awac,
            'SSDT-HPET': HardwareGenerators.generate_hpet,
            'SSDT-PMC': HardwareGenerators.generate_pmc,
            'SSDT-SBUS': HardwareGenerators.generate_sbus,
            'SSDT-PNLF': LaptopGenerators.generate_pnlf,
            'SSDT-ALS0': LaptopGenerators.generate_als0,
            'SSDT-GPI0': LaptopGenerators.generate_gpi0,
            'SSDT-USBX': USBGenerators.generate_usbx,
            'SSDT-USB-Reset': USBGenerators.generate_usb_reset,
            'SSDT-XOSI': AdvancedGenerators.generate_xosi,
            'SSDT-GPU-DISABLE': AdvancedGenerators.generate_gpu_disable,
            'SSDT-GPU-SPOOF': AdvancedGenerators.generate_gpu_spoof,
            'SSDT-dGPU-Off': AdvancedGenerators.generate_dgpu_off,
            'SSDT-NoHybGfx': AdvancedGenerators.generate_nohybgfx,
            'SSDT-RHUB': AdvancedGenerators.generate_rhub,
            'SSDT-RHUB-prebuilt': AdvancedGenerators.generate_rhub_prebuilt,
            'SSDT-UNC': AdvancedGenerators.generate_unc,
            'SSDT-RTC0-RANGE': AdvancedGenerators.generate_rtc0_range,
            'SSDT-CPUR': AdvancedGenerators.generate_cpur,
            'SSDT-IMEI': AdvancedGenerators.generate_imei,
            'SSDT-EC-USBX-DESKTOP': AdvancedGenerators.generate_ec_usbx_desktop,
            'SSDT-EC-USBX-LAPTOP': AdvancedGenerators.generate_ec_usbx_laptop,
            'SSDT-PLUG-DRTNIA': AdvancedGenerators.generate_plug_drtnia,
        }
        
        generator = generators.get(patch_name)
        if generator:
            # Pass DSDT context to generator
            return generator(output_path, dsdt_context)
        else:
            # Use generic template loader for patches without specific generators
            return AdvancedGenerators.generate_from_template(patch_name, output_path)
    
    def clear_selection(self):
        """Clear all selections"""
        for patch in self.main_app.patch_manager.patches:
            patch.checked = False
            if patch.name in self.patch_vars:
                self.patch_vars[patch.name].set(False)
        
        self.main_app.update_status("Selection cleared")
    
    def refresh(self):
        """Refresh the tab"""
        self.populate_patches()
