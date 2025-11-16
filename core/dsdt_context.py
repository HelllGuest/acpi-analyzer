"""DSDT Context Manager - Stores detected device paths"""


class DSDTContext:
    """Manages DSDT-specific device paths for patch generation"""
    
    def __init__(self, acpi_parser=None):
        self.parser = acpi_parser
        self.pci_root = None
        self.lpc_bridge = None
        self.gpu_device = None
        self.cpu_path = None
        self.usb_controller = None
        self.smbus = None
        self.ec_device = None
        self.battery_device = None
        self.hpet_device = None
        self.gpio_device = None
        self.analyzed = False
    
    def analyze(self):
        """Analyze DSDT and extract all device paths"""
        if not self.parser:
            return False
        
        paths = self.parser.get_device_paths()
        
        self.pci_root = paths.get('pci_root')
        self.lpc_bridge = paths.get('lpc_bridge')
        self.gpu_device = paths.get('gpu_device')
        self.cpu_path = paths.get('cpu_path')
        self.usb_controller = paths.get('usb_controller')
        self.smbus = paths.get('smbus')
        self.ec_device = paths.get('ec_device')
        self.battery_device = paths.get('battery_device')
        self.hpet_device = paths.get('hpet_device')
        self.gpio_device = paths.get('gpio_device')
        
        self.analyzed = True
        return True
    
    def get_ec_parent_path(self, default="_SB.PCI0.LPCB"):
        """Get path where EC should be created"""
        if self.lpc_bridge:
            return self.lpc_bridge
        return default
    
    def get_gpu_path(self, default="_SB.PCI0.GFX0"):
        """Get GPU device path"""
        if self.gpu_device:
            return self.gpu_device
        return default
    
    def get_cpu_path(self, default="_PR.CPU0"):
        """Get CPU processor path"""
        if self.cpu_path:
            return self.cpu_path
        return default
    
    def get_usb_path(self, default="_SB.PCI0.XHC"):
        """Get USB controller path"""
        if self.usb_controller:
            return self.usb_controller
        return default
    
    def get_smbus_path(self, default="_SB.PCI0.SBUS"):
        """Get SMBus device path"""
        if self.smbus:
            return self.smbus
        return default
    
    def get_hpet_path(self, default="_SB.PCI0.LPCB.HPET"):
        """Get HPET device path"""
        if self.hpet_device:
            return self.hpet_device
        if self.lpc_bridge:
            return f"{self.lpc_bridge}.HPET"
        return default
    
    def get_gpio_path(self, default="_SB.PCI0.GPI0"):
        """Get GPIO device path"""
        if self.gpio_device:
            return self.gpio_device
        return default
    
    def has_device(self, device_type):
        """Check if device was detected"""
        device_map = {
            'pci_root': self.pci_root,
            'lpc_bridge': self.lpc_bridge,
            'gpu': self.gpu_device,
            'cpu': self.cpu_path,
            'usb': self.usb_controller,
            'smbus': self.smbus,
            'ec': self.ec_device,
            'battery': self.battery_device,
            'hpet': self.hpet_device,
            'gpio': self.gpio_device
        }
        return device_map.get(device_type) is not None
    
    def get_detection_summary(self):
        """Get summary of detected devices"""
        return {
            'PCI Root': self.pci_root or 'Not found',
            'LPC Bridge': self.lpc_bridge or 'Not found',
            'GPU Device': self.gpu_device or 'Not found',
            'CPU Path': self.cpu_path or 'Not found',
            'USB Controller': self.usb_controller or 'Not found',
            'SMBus': self.smbus or 'Not found',
            'EC Device': self.ec_device or 'Not found',
            'Battery Device': self.battery_device or 'Not found',
            'HPET Device': self.hpet_device or 'Not found',
            'GPIO Device': self.gpio_device or 'Not found'
        }
    
    def get_compatibility_status(self, patch_name):
        """Get compatibility status for a patch"""
        # Map patches to required devices
        patch_requirements = {
            'SSDT-EC': 'lpc_bridge',
            'SSDT-PLUG': 'cpu',
            'SSDT-AWAC': 'pci_root',
            'SSDT-HPET': 'hpet',
            'SSDT-PMC': 'lpc_bridge',
            'SSDT-SBUS': 'smbus',
            'SSDT-PNLF': 'gpu',
            'SSDT-ALS0': 'lpc_bridge',
            'SSDT-GPI0': 'gpio',
            'SSDT-USBX': 'usb',
            'SSDT-USB-Reset': 'usb'
        }
        
        required_device = patch_requirements.get(patch_name)
        if not required_device:
            return 'generic'  # No specific device required
        
        if self.has_device(required_device):
            return 'compatible'  # Device found
        else:
            return 'generic_fallback'  # Will use generic path
