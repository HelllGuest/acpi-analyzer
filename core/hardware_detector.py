"""Hardware detection system"""

import platform
import os


class HardwareDetector:
    """Detect hardware and recommend patches"""

    def __init__(self, acpi_parser):
        self.acpi_parser = acpi_parser
        self.cpu_info = None
        self.platform_type = None
        self.chipset_info = None

    def detect(self):
        """Detect hardware and return information"""
        self.detect_cpu()
        self.detect_platform()
        self.detect_chipset()
        
        recommended = self.get_recommended_patches()
        
        return {
            'cpu': self.cpu_info or 'Unknown',
            'platform': self.platform_type or 'Unknown',
            'chipset': self.chipset_info or 'Unknown',
            'recommended_patches': recommended
        }

    def detect_cpu(self):
        """Detect CPU information"""
        try:
            cpu = platform.processor()
            if 'Intel' in cpu:
                self.cpu_info = 'Intel'
            elif 'AMD' in cpu:
                self.cpu_info = 'AMD'
            else:
                self.cpu_info = cpu if cpu else 'Unknown'
        except Exception:
            self.cpu_info = 'Unknown'

    def detect_platform(self):
        """Detect platform type based on ACPI battery device"""
        if self.acpi_parser and self.acpi_parser.find_battery_device():
            self.platform_type = 'Laptop'
        else:
            self.platform_type = 'Desktop'

    def detect_chipset(self):
        """Detect chipset information"""
        self.chipset_info = 'Intel 300+ Series (Assumed)'
    
    def get_recommended_patches(self):
        """Get recommended patches based on hardware"""
        recommended = []
        
        # Essential patches for all systems
        recommended.extend(['SSDT-EC', 'SSDT-PLUG'])
        
        # Platform-specific
        if self.platform_type == 'Laptop':
            recommended.extend(['SSDT-PNLF', 'SSDT-GPI0', 'SSDT-ALS0'])
        
        # Chipset-specific
        if '300' in str(self.chipset_info) or '400' in str(self.chipset_info):
            recommended.extend(['SSDT-AWAC', 'SSDT-PMC'])
        
        # Common recommendations
        recommended.extend(['SSDT-HPET', 'SSDT-SBUS', 'SSDT-USBX'])
        
        return recommended
