"""ACPI file parsing and analysis"""

import re


class ACPIParser:
    """Parse and analyze ACPI tables"""
    
    def __init__(self):
        self.devices = []
        self.methods = []
        self.scopes = []
        self.current_file = None
        self.content = None
    
    def parse_file(self, filepath):
        """Parse an ACPI DSL file"""
        self.current_file = filepath
        self.devices = []
        self.methods = []
        self.scopes = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                self.content = f.read()
            
            self._extract_devices(self.content)
            self._extract_methods(self.content)
            self._extract_scopes(self.content)
            
            return True
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return False
    
    def _extract_devices(self, content):
        """Extract device definitions"""
        # Match Device (NAME) { ... }
        device_pattern = r'Device\s*\(([A-Z0-9_]+)\)'
        matches = re.finditer(device_pattern, content)
        
        for match in matches:
            device_name = match.group(1)
            start_pos = match.start()
            
            # Try to find _HID or _ADR
            context = content[start_pos:start_pos+500]
            hid_match = re.search(r'_HID,?\s*"?([A-Z0-9]+)"?', context)
            adr_match = re.search(r'_ADR,?\s*(0x[0-9A-Fa-f]+)', context)
            
            device_info = {
                'name': device_name,
                'hid': hid_match.group(1) if hid_match else None,
                'adr': adr_match.group(1) if adr_match else None,
                'position': start_pos
            }
            self.devices.append(device_info)
    
    def _extract_methods(self, content):
        """Extract method definitions"""
        # Match Method (NAME, ...) { ... }
        method_pattern = r'Method\s*\(([A-Z0-9_]+)'
        matches = re.finditer(method_pattern, content)
        
        for match in matches:
            self.methods.append({
                'name': match.group(1),
                'position': match.start()
            })
    
    def _extract_scopes(self, content):
        """Extract scope definitions"""
        # Match Scope (\_SB.PCI0.XXX) { ... }
        scope_pattern = r'Scope\s*\(([\\._A-Z0-9]+)\)'
        matches = re.finditer(scope_pattern, content)
        
        for match in matches:
            self.scopes.append({
                'path': match.group(1),
                'position': match.start()
            })
    
    def find_device_by_hid(self, hid):
        """Find devices with specific HID"""
        return [d for d in self.devices if d.get('hid') == hid]
    
    def find_device_by_name(self, name):
        """Find device by name"""
        return [d for d in self.devices if d.get('name') == name]
    
    def get_all_devices(self):
        """Get all discovered devices"""
        return self.devices
    
    def get_device_count(self):
        """Get total device count"""
        return len(self.devices)
    
    def export_to_dict(self):
        """Export parsed data to dictionary"""
        return {
            'file': str(self.current_file) if self.current_file else None,
            'devices': self.devices,
            'methods': self.methods,
            'scopes': self.scopes,
            'stats': {
                'device_count': len(self.devices),
                'method_count': len(self.methods),
                'scope_count': len(self.scopes)
            }
        }
    
    def find_pci_root(self):
        """Find PCI root device (PCI0, PC00, PCIO, etc.)"""
        if not self.content:
            return None
        
        # Common PCI root names
        pci_names = ['PCI0', 'PC00', 'PCIO', 'PCI1', 'PCIE']
        
        for name in pci_names:
            # Look for Device (NAME) or Scope (\_SB.NAME)
            pattern = rf'(?:Device|Scope)\s*\((?:[\\._]*SB[\\._])?({name})\)'
            match = re.search(pattern, self.content)
            if match:
                return f"_SB.{name}"
        
        return None
    
    def find_lpc_bridge(self):
        """Find LPC bridge device (LPCB, LPC0, SBRG, etc.)"""
        if not self.content:
            return None
        
        # Common LPC bridge names
        lpc_names = ['LPCB', 'LPC0', 'LPC', 'SBRG', 'LPCB0']
        pci_root = self.find_pci_root()
        
        if not pci_root:
            return None
        
        for name in lpc_names:
            # Look for Device under PCI root
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return f"{pci_root}.{name}"
        
        return None
    
    def find_gpu_device(self):
        """Find GPU device (GFX0, IGPU, VID, VGA, etc.)"""
        if not self.content:
            return None
        
        # Common GPU names
        gpu_names = ['GFX0', 'IGPU', 'VID', 'VGA', 'GFX', 'VID0']
        pci_root = self.find_pci_root()
        
        if not pci_root:
            return None
        
        for name in gpu_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return f"{pci_root}.{name}"
        
        return None
    
    def find_cpu_path(self):
        """Find CPU processor path (_PR.CPU0, _SB.PR00, _SB.CP00, etc.)"""
        if not self.content:
            return None
        
        # Look for Processor declarations
        # Pattern: Processor (CPU0, 0x01, 0x00000410, 0x06)
        processor_pattern = r'Processor\s*\(([A-Z0-9]+),'
        match = re.search(processor_pattern, self.content)
        if match:
            cpu_name = match.group(1)
            # Check if it's under _PR or _SB
            if re.search(rf'Scope\s*\([\\._]*PR\)', self.content):
                return f"_PR.{cpu_name}"
            elif re.search(rf'Scope\s*\([\\._]*SB\)', self.content):
                return f"_SB.{cpu_name}"
            return f"_PR.{cpu_name}"
        
        # Look for Device-based CPU (newer ACPI)
        cpu_names = ['CPU0', 'CP00', 'PR00', 'C000', 'P000']
        for name in cpu_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                if re.search(rf'Scope\s*\([\\._]*PR\)', self.content):
                    return f"_PR.{name}"
                return f"_SB.{name}"
        
        return None
    
    def find_usb_controller(self):
        """Find USB controller (XHC, XHCI, XHC1, EHC1, EHC2, etc.)"""
        if not self.content:
            return None
        
        # Common USB controller names
        usb_names = ['XHC', 'XHCI', 'XHC1', 'XHC0', 'XHCX', 'EHC1', 'EHC2']
        pci_root = self.find_pci_root()
        
        if not pci_root:
            return None
        
        for name in usb_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return f"{pci_root}.{name}"
        
        return None
    
    def find_smbus(self):
        """Find SMBus device (SBUS, SMBU, SMBS, etc.)"""
        if not self.content:
            return None
        
        # Common SMBus names
        smbus_names = ['SBUS', 'SMBU', 'SMBS', 'SBUS0', 'SMBU0']
        pci_root = self.find_pci_root()
        
        if not pci_root:
            return None
        
        for name in smbus_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return f"{pci_root}.{name}"
        
        return None
    
    def find_ec_device(self):
        """Find existing Embedded Controller device"""
        if not self.content:
            return None
        
        # Look for devices with EC-related HID
        ec_hids = ['PNP0C09']
        for hid in ec_hids:
            devices = self.find_device_by_hid(hid)
            if devices:
                return devices[0]['name']
        
        # Look for common EC device names
        ec_names = ['EC0', 'EC', 'H_EC', 'ECDV', 'PGEC']
        for name in ec_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return name
        
        return None
    
    def find_battery_device(self):
        """Find battery device"""
        if not self.content:
            return None
        
        # Look for devices with battery HID
        battery_hids = ['PNP0C0A']
        for hid in battery_hids:
            devices = self.find_device_by_hid(hid)
            if devices:
                return devices[0]['name']
        
        # Look for common battery names
        battery_names = ['BAT0', 'BAT1', 'BATC', 'BATT']
        for name in battery_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return name
        
        return None
    
    def find_hpet_device(self):
        """Find HPET device"""
        if not self.content:
            return None
        
        lpc_bridge = self.find_lpc_bridge()
        if not lpc_bridge:
            return None
        
        # Look for HPET device
        hpet_names = ['HPET', 'HPE0', 'HPET0']
        for name in hpet_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return f"{lpc_bridge}.{name}"
        
        return None
    
    def find_gpio_device(self):
        """Find GPIO device (GPI0, GPIO, etc.)"""
        if not self.content:
            return None
        
        pci_root = self.find_pci_root()
        if not pci_root:
            return None
        
        # Common GPIO names
        gpio_names = ['GPI0', 'GPIO', 'GPI1']
        for name in gpio_names:
            pattern = rf'Device\s*\({name}\)'
            if re.search(pattern, self.content):
                return f"{pci_root}.{name}"
        
        return None
    
    def get_device_paths(self):
        """Get all detected device paths"""
        return {
            'pci_root': self.find_pci_root(),
            'lpc_bridge': self.find_lpc_bridge(),
            'gpu_device': self.find_gpu_device(),
            'cpu_path': self.find_cpu_path(),
            'usb_controller': self.find_usb_controller(),
            'smbus': self.find_smbus(),
            'ec_device': self.find_ec_device(),
            'battery_device': self.find_battery_device(),
            'hpet_device': self.find_hpet_device(),
            'gpio_device': self.find_gpio_device()
        }
