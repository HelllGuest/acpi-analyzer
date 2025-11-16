"""SSDT generators for various patches"""

from .essential_generators import EssentialGenerators
from .hardware_generators import HardwareGenerators
from .laptop_generators import LaptopGenerators
from .usb_generators import USBGenerators
from .advanced_generators import AdvancedGenerators

__all__ = ['EssentialGenerators', 'HardwareGenerators', 'LaptopGenerators', 'USBGenerators', 'AdvancedGenerators']
