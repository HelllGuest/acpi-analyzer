"""Device ID database for hardware identification"""

DEVICE_DATABASE = {
    # Embedded Controllers
    'PNP0C09': {'name': 'Embedded Controller', 'category': 'System', 'critical': True},
    
    # System Devices
    'PNP0000': {'name': 'Programmable Interrupt Controller', 'category': 'System', 'critical': True},
    'PNP0100': {'name': 'System Timer', 'category': 'System', 'critical': True},
    'PNP0103': {'name': 'HPET', 'category': 'System', 'critical': True},
    'PNP0200': {'name': 'DMA Controller', 'category': 'System', 'critical': False},
    'PNP0B00': {'name': 'RTC', 'category': 'System', 'critical': True},
    'PNP0C01': {'name': 'System Board', 'category': 'System', 'critical': False},
    'PNP0C02': {'name': 'Motherboard Resources', 'category': 'System', 'critical': False},
    'PNP0C04': {'name': 'Math Coprocessor', 'category': 'System', 'critical': False},
    'PNP0C0C': {'name': 'Power Button', 'category': 'System', 'critical': False},
    'PNP0C0D': {'name': 'Lid Switch', 'category': 'Laptop', 'critical': False},
    'PNP0C0E': {'name': 'Sleep Button', 'category': 'System', 'critical': False},
    'PNP0C0F': {'name': 'PCI Interrupt Link', 'category': 'System', 'critical': True},
    
    # Storage
    'PNP0600': {'name': 'IDE Controller', 'category': 'Storage', 'critical': False},
    'PNP0700': {'name': 'Floppy Controller', 'category': 'Storage', 'critical': False},
    
    # Input Devices
    'PNP0303': {'name': 'Keyboard', 'category': 'Input', 'critical': False},
    'PNP0F03': {'name': 'PS/2 Mouse', 'category': 'Input', 'critical': False},
    'PNP0F13': {'name': 'PS/2 Port', 'category': 'Input', 'critical': False},
    
    # Communication
    'PNP0400': {'name': 'LPT Port', 'category': 'Communication', 'critical': False},
    'PNP0500': {'name': 'COM Port', 'category': 'Communication', 'critical': False},
    'PNP0501': {'name': '16550A UART', 'category': 'Communication', 'critical': False},
    
    # Audio
    'HDAUDIO': {'name': 'HD Audio', 'category': 'Audio', 'critical': False},
    'INTC': {'name': 'Intel Audio', 'category': 'Audio', 'critical': False},
    
    # Intel Devices
    'INT33A1': {'name': 'Intel Power Engine', 'category': 'Power', 'critical': False},
    'INT3400': {'name': 'Intel DPTF', 'category': 'Thermal', 'critical': False},
    'INT3403': {'name': 'DPTF Temperature Sensor', 'category': 'Thermal', 'critical': False},
    'INT3F0D': {'name': 'Intel Ambient Light Sensor', 'category': 'Sensor', 'critical': False},
    'INT34BB': {'name': 'Intel Bluetooth', 'category': 'Wireless', 'critical': False},
    
    # ACPI Devices
    'ACPI0003': {'name': 'AC Adapter', 'category': 'Power', 'critical': False},
    'ACPI0008': {'name': 'Ambient Light Sensor', 'category': 'Sensor', 'critical': False},
    'ACPI000C': {'name': 'Power Button', 'category': 'Input', 'critical': False},
    'ACPI000D': {'name': 'Lid Device', 'category': 'Laptop', 'critical': False},
    'ACPI000E': {'name': 'Sleep Button', 'category': 'Input', 'critical': False},
    'PNP0C0A': {'name': 'Control Method Battery', 'category': 'Power', 'critical': True},
    'PNP0A08': {'name': 'PCI Express Root Complex', 'category': 'System', 'critical': True},
    'PNP0C14': {'name': 'SMBus Host Controller', 'category': 'System', 'critical': False},
    'INTC9C60': {'name': 'Intel Smart Sound Technology', 'category': 'Audio', 'critical': False},
    'INTC9C61': {'name': 'Intel Smart Sound Technology', 'category': 'Audio', 'critical': False},
    'INTC9C62': {'name': 'Intel Smart Sound Technology', 'category': 'Audio', 'critical': False},
    'INTC10EC': {'name': 'Intel High Definition Audio', 'category': 'Audio', 'critical': False},
    'DELL05E8': {'name': 'Dell Airplane Mode Switch', 'category': 'Wireless', 'critical': False},
    'DELL06F1': {'name': 'Dell System Management', 'category': 'System', 'critical': False},
    'DELL07A0': {'name': 'Dell Wireless Hotkey', 'category': 'Wireless', 'critical': False},
    'LEN0071': {'name': 'Lenovo Power Management', 'category': 'Power', 'critical': False},
    'LEN0268': {'name': 'Lenovo ThinkPad Extra Bits', 'category': 'System', 'critical': False},
}

CPU_DATABASE = {
    # Intel CPUs
    'Intel': {
        'Haswell': {'generation': 4, 'year': 2013, 'xcpm': True},
        'Broadwell': {'generation': 5, 'year': 2014, 'xcpm': True},
        'Skylake': {'generation': 6, 'year': 2015, 'xcpm': True},
        'Kaby Lake': {'generation': 7, 'year': 2017, 'xcpm': True},
        'Coffee Lake': {'generation': 8, 'year': 2017, 'xcpm': True},
        'Comet Lake': {'generation': 10, 'year': 2020, 'xcpm': True},
        'Rocket Lake': {'generation': 11, 'year': 2021, 'xcpm': True},
        'Alder Lake': {'generation': 12, 'year': 2021, 'xcpm': True},
    }
}

CHIPSET_DATABASE = {
    'Intel': {
        'Z370': {'series': 300, 'requires_awac': True, 'requires_pmc': True},
        'Z390': {'series': 300, 'requires_awac': True, 'requires_pmc': True},
        'Z490': {'series': 400, 'requires_awac': True, 'requires_pmc': True},
        'Z590': {'series': 500, 'requires_awac': True, 'requires_pmc': True},
        'Z690': {'series': 600, 'requires_awac': True, 'requires_pmc': True},
    }
}

def get_device_info(device_id):
    """Get information about a device ID"""
    return DEVICE_DATABASE.get(device_id, {'name': 'Unknown Device', 'category': 'Unknown', 'critical': False})

def is_critical_device(device_id):
    """Check if device is critical for macOS"""
    info = get_device_info(device_id)
    return info.get('critical', False)
