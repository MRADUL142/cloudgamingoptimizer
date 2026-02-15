"""Data Collection package initializer.

Keep this file minimal so submodules can be imported lazily by callers.
Importing heavy dependencies (like `psutil`) inside submodules will not
prevent importing the package itself.
"""

from .network_metrics import NetworkMetricsCollector
from .system_metrics import SystemMetricsCollector
from .data_logger import DataLogger

__all__ = [
    'NetworkMetricsCollector',
    'SystemMetricsCollector',
    'DataLogger'
]
