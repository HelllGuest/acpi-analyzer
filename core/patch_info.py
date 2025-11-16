"""Patch information and management system"""

class PatchInfo:
    """Information about an SSDT patch"""
    
    def __init__(self, name, description, category, priority, dependencies=None, 
                 platforms=None, requires_hardware=None):
        self.name = name
        self.description = description
        self.category = category
        self.priority = priority
        self.dependencies = dependencies or []
        self.platforms = platforms or ['Desktop', 'Laptop']
        self.requires_hardware = requires_hardware or []
        self.checked = False
        self.generated = False
        self.recommended = False
    
    def __repr__(self):
        return f"PatchInfo({self.name}, {self.category}, {self.priority})"


class PatchManager:
    """Manages all available patches"""
    
    def __init__(self):
        self.patches = []
        self._initialize_patches()
    
    def _initialize_patches(self):
        """Initialize all available patches"""
        # Essential patches
        self.patches.extend([
            PatchInfo(
                "SSDT-EC",
                "Fake Embedded Controller - REQUIRED for Catalina+",
                "Essential",
                "critical",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-PLUG",
                "CPU Power Management - REQUIRED for proper CPU PM",
                "Essential",
                "critical",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-AWAC",
                "System Clock Fix - Required for 300+ series",
                "Essential",
                "high",
                platforms=['Desktop', 'Laptop']
            ),
        ])
        
        # Hardware patches
        self.patches.extend([
            PatchInfo(
                "SSDT-HPET",
                "IRQ Conflict Resolution - Fixes audio/USB issues",
                "Hardware",
                "high",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-PMC",
                "NVRAM Support - Required for 300+ series",
                "Hardware",
                "high",
                platforms=['Desktop']
            ),
            PatchInfo(
                "SSDT-SBUS",
                "System Management Bus - Recommended",
                "Hardware",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-MCHC",
                "Memory Controller - Cosmetic fix",
                "Hardware",
                "low",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-IMEI",
                "Management Engine Interface",
                "Hardware",
                "low",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-DMAC",
                "DMA Controller - Cosmetic",
                "Hardware",
                "low",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-MEM2",
                "Memory Controller 2",
                "Hardware",
                "low",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-PPMC",
                "Platform Power Management Controller",
                "Hardware",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
        ])
        
        # Laptop patches
        self.patches.extend([
            PatchInfo(
                "SSDT-PNLF",
                "Backlight Control - REQUIRED for laptops",
                "Laptop",
                "critical",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-ALS0",
                "Ambient Light Sensor",
                "Laptop",
                "medium",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-GPI0",
                "GPIO Controller for I2C devices",
                "Laptop",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-XOSI",
                "OS Interface patches for Windows features",
                "Laptop",
                "medium",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-PRW",
                "Instant Wake Fix - Prevents instant wake",
                "Laptop",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-Battery",
                "Battery Status Reporting",
                "Laptop",
                "high",
                platforms=['Laptop']
            ),
        ])
        
        # USB patches
        self.patches.extend([
            PatchInfo(
                "SSDT-USBX",
                "USB Power Properties - Recommended",
                "USB",
                "high",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-USB-Reset",
                "Reset USB Hubs",
                "USB",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
        ])
        
        # Advanced patches
        self.patches.extend([
            PatchInfo(
                "SSDT-XOSI",
                "OS Interface patches - Windows compatibility",
                "Advanced",
                "medium",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-GPU-DISABLE",
                "Disable Discrete GPU - For laptops with dual GPU",
                "Advanced",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-GPU-SPOOF",
                "Spoof GPU Device ID - For unsupported GPUs",
                "Advanced",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-dGPU-Off",
                "Alternative Discrete GPU Disable",
                "Advanced",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-NoHybGfx",
                "Disable Hybrid Graphics - For Optimus laptops",
                "Advanced",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-RHUB",
                "USB Hub Reset - Alternative USB fix",
                "Advanced",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-RHUB-prebuilt",
                "USB Hub Reset Prebuilt - Alternative version",
                "Advanced",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-UNC",
                "Uncore Bridge - HEDT systems only",
                "Advanced",
                "optional",
                platforms=['Desktop']
            ),
            PatchInfo(
                "SSDT-RTC0-RANGE",
                "RTC Range Fix - HEDT systems",
                "Advanced",
                "optional",
                platforms=['Desktop']
            ),
            PatchInfo(
                "SSDT-CPUR",
                "CPU Renaming - For specific systems",
                "Advanced",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-IMEI",
                "Intel Management Engine Interface",
                "Advanced",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-EC-USBX-DESKTOP",
                "Combined EC and USBX - Desktop all-in-one",
                "Advanced",
                "optional",
                platforms=['Desktop']
            ),
            PatchInfo(
                "SSDT-EC-USBX-LAPTOP",
                "Combined EC and USBX - Laptop all-in-one",
                "Advanced",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-PLUG-DRTNIA",
                "Alternative PLUG Implementation",
                "Advanced",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
        ])
        
        # Battery patches
        self.patches.extend([
            PatchInfo(
                "SSDT-BATS",
                "Battery Status - Generic implementation",
                "Battery",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-BATT",
                "Battery Status - Alternative",
                "Battery",
                "high",
                platforms=['Laptop']
            ),
        ])
        
        # Trackpad patches
        self.patches.extend([
            PatchInfo(
                "SSDT-I2C0-TPXX",
                "I2C Trackpad - Generic",
                "Trackpad",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-I2C1-TPXX",
                "I2C Trackpad - Alternative bus",
                "Trackpad",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-ThinkPad_ClickPad",
                "ThinkPad ClickPad support",
                "Trackpad",
                "medium",
                platforms=['Laptop']
            ),
        ])
        
        # Display patches
        self.patches.extend([
            PatchInfo(
                "SSDT-PNLF-CFL",
                "Backlight - Coffee Lake",
                "Display",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-PNLF-SKL_KBL",
                "Backlight - Skylake/Kaby Lake",
                "Display",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-PNLF-Haswell_Broadwell",
                "Backlight - Haswell/Broadwell",
                "Display",
                "high",
                platforms=['Laptop']
            ),
        ])
        
        # Graphics patches
        self.patches.extend([
            PatchInfo(
                "SSDT-DGPU",
                "Disable Discrete GPU - Generic",
                "Graphics",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-NDGP_OFF",
                "Disable NVIDIA GPU",
                "Graphics",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-RX580",
                "AMD RX 580 GPU support",
                "Graphics",
                "optional",
                platforms=['Desktop']
            ),
        ])
        
        # Power management patches
        self.patches.extend([
            PatchInfo(
                "SSDT-GPRW",
                "Instant Wake Fix - Generic",
                "Power",
                "high",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-PTSWAKTTS",
                "Sleep/Wake Fix - Comprehensive",
                "Power",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-LIDpatch",
                "Lid Wake Fix",
                "Power",
                "medium",
                platforms=['Laptop']
            ),
        ])
        
        # Input device patches
        self.patches.extend([
            PatchInfo(
                "SSDT-RMCF-PS2Map-AtoZ",
                "PS2 Keyboard Mapping",
                "Input",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-BKeyQ11Q12",
                "Brightness Keys - Lenovo",
                "Input",
                "optional",
                platforms=['Laptop']
            ),
        ])
        
        # Hardware device patches
        self.patches.extend([
            PatchInfo(
                "SSDT-SBUS-MCHC",
                "Combined SBUS and MCHC",
                "Hardware",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-DMAC",
                "DMA Controller",
                "Hardware",
                "low",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-PMCR",
                "PMC Device - Alternative",
                "Hardware",
                "medium",
                platforms=['Desktop']
            ),
        ])
        
        # Compatibility patches
        self.patches.extend([
            PatchInfo(
                "SSDT-OC-XOSI",
                "OpenCore XOSI - OS compatibility",
                "Compatibility",
                "medium",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-Darwin",
                "Darwin OS detection",
                "Compatibility",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
        ])
        
        # Additional specific patches from extended collection
        self.patches.extend([
            PatchInfo(
                "SSDT-UPRW",
                "USB Power Wake Fix - Alternative to GPRW",
                "Power",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-XPRW",
                "Extended Power Wake Fix",
                "Power",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-DeepIdle",
                "Deep Idle Power Management",
                "Power",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-PWRB",
                "Power Button Device",
                "Power",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-SLPB",
                "Sleep Button Device",
                "Power",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-OCBAT0-TP",
                "ThinkPad Battery Patch",
                "Battery",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-OCBAT0-HP",
                "HP Battery Patch",
                "Battery",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-OCBAT0-ASUS",
                "ASUS Battery Patch",
                "Battery",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-OCI2C-TPXX",
                "I2C Trackpad - OpenCore Generic",
                "Trackpad",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-PNLF-SNB_IVY",
                "Backlight - Sandy Bridge/Ivy Bridge",
                "Display",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-PNLF-ACPI",
                "Backlight - ACPI Method",
                "Display",
                "high",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-NDGP_PS3",
                "NVIDIA GPU Power State 3",
                "Graphics",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-EHCx_OFF",
                "Disable EHC Controllers",
                "USB",
                "optional",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-RMCF-PS2Map-dell",
                "PS2 Keyboard Mapping - Dell",
                "Input",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-RMCF-PS2Map-Lenovo",
                "PS2 Keyboard Mapping - Lenovo",
                "Input",
                "optional",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-ThinkPad_TrackPad",
                "ThinkPad TrackPad Support",
                "Trackpad",
                "medium",
                platforms=['Laptop']
            ),
            PatchInfo(
                "SSDT-HPET_RTC_TIMR-fix",
                "HPET/RTC/TIMR IRQ Fix",
                "Hardware",
                "high",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-SMBU",
                "SMBus Device - Alternative",
                "Hardware",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-RTC0-NoFlags",
                "RTC Device without Flags",
                "Hardware",
                "medium",
                platforms=['Desktop', 'Laptop']
            ),
            PatchInfo(
                "SSDT-IPIC",
                "Interrupt Controller",
                "Hardware",
                "low",
                platforms=['Desktop', 'Laptop']
            ),
        ])
    
    def get_patches_by_category(self, category):
        """Get all patches in a category"""
        return [p for p in self.patches if p.category == category]
    
    def get_patches_by_platform(self, platform):
        """Get patches suitable for platform"""
        return [p for p in self.patches if platform in p.platforms]
    
    def get_checked_patches(self):
        """Get all checked patches"""
        return [p for p in self.patches if p.checked]
    
    def get_recommended_patches(self):
        """Get all recommended patches"""
        return [p for p in self.patches if p.recommended]
    
    def get_stats(self):
        """Get patch statistics"""
        return {
            'total': len(self.patches),
            'checked': len([p for p in self.patches if p.checked]),
            'generated': len([p for p in self.patches if p.generated]),
            'recommended': len([p for p in self.patches if p.recommended]),
            'categories': len(set(p.category for p in self.patches)),
        }
    
    def reset_all(self):
        """Reset all patch states"""
        for patch in self.patches:
            patch.checked = False
            patch.generated = False
            patch.recommended = False
