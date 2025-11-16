"""Core functionality for Acpi Analyzer"""

from .patch_info import PatchManager, PatchInfo
from .acpi_parser import ACPIParser
from .hardware_detector import HardwareDetector
from .dsdt_context import DSDTContext

__all__ = ['PatchManager', 'PatchInfo', 'HardwareDetector', 'ACPIParser', 'DSDTContext']
