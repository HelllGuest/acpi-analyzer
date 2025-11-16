"""Data module for device and hardware databases"""

from .device_database import DEVICE_DATABASE, CPU_DATABASE, CHIPSET_DATABASE
from .device_database import get_device_info, is_critical_device

__all__ = ['DEVICE_DATABASE', 'CPU_DATABASE', 'CHIPSET_DATABASE', 
           'get_device_info', 'is_critical_device']
