"""System Metrics Collection - CPU, GPU, RAM usage."""

import logging
from datetime import datetime
from typing import Dict, List
import json

logger = logging.getLogger(__name__)


class SystemMetricsCollector:
    """Collects system performance metrics."""
    
    def __init__(self):
        """Initialize system metrics collector."""
        self.metrics_history: List[Dict] = []
    
    def get_cpu_metrics(self) -> Dict[str, float]:
        """
        Collect CPU metrics.
        
        Returns:
            Dictionary with cpu_percent, per_core_percent
        """
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)
            per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
            cpu_count = psutil.cpu_count(logical=True)

            metrics = {
                "cpu_percent": round(cpu_percent, 2),
                "per_core_percent": [round(x, 2) for x in per_cpu],
                "cpu_count": cpu_count,
                "cpu_freq_ghz": round(psutil.cpu_freq().current / 1000, 2) if psutil.cpu_freq() else 0
            }

            logger.debug(f"CPU metrics: {metrics}")
            return metrics

        except ImportError:
            logger.warning("psutil not installed, CPU metrics unavailable")
            return {
                "cpu_percent": 0,
                "per_core_percent": [],
                "cpu_count": 0,
                "cpu_freq_ghz": 0
            }
        except Exception as e:
            logger.error(f"Error collecting CPU metrics: {e}")
            return {
                "cpu_percent": 0,
                "per_core_percent": [],
                "cpu_count": 0,
                "cpu_freq_ghz": 0
            }
    
    def get_memory_metrics(self) -> Dict[str, float]:
        """
        Collect memory metrics.
        
        Returns:
            Dictionary with ram_percent, ram_used_gb, ram_available_gb
        """
        try:
            import psutil

            memory = psutil.virtual_memory()

            metrics = {
                "ram_percent": round(memory.percent, 2),
                "ram_used_gb": round(memory.used / (1024**3), 2),
                "ram_total_gb": round(memory.total / (1024**3), 2),
                "ram_available_gb": round(memory.available / (1024**3), 2)
            }

            logger.debug(f"Memory metrics: {metrics}")
            return metrics

        except ImportError:
            logger.warning("psutil not installed, memory metrics unavailable")
            return {
                "ram_percent": 0,
                "ram_used_gb": 0,
                "ram_total_gb": 0,
                "ram_available_gb": 0
            }
        except Exception as e:
            logger.error(f"Error collecting memory metrics: {e}")
            return {
                "ram_percent": 0,
                "ram_used_gb": 0,
                "ram_total_gb": 0,
                "ram_available_gb": 0
            }
    
    def get_gpu_metrics(self) -> Dict[str, float]:
        """
        Collect GPU metrics using GPUtil.
        
        Returns:
            Dictionary with gpu_percent, gpu_memory_percent
        """
        try:
            import GPUtil  # type: ignore
            
            gpus = GPUtil.getGPUs()
            
            if not gpus:
                return {
                    "gpu_available": False,
                    "gpu_percent": 0,
                    "gpu_memory_percent": 0,
                    "gpu_count": 0
                }
            
            gpu = gpus[0]  # Use first GPU
            
            metrics = {
                "gpu_available": True,
                "gpu_percent": round(gpu.load * 100, 2),
                "gpu_memory_percent": round(gpu.memoryUtil * 100, 2),
                "gpu_memory_used_gb": round(gpu.memoryUsed / 1024, 2),
                "gpu_memory_total_gb": round(gpu.memoryTotal / 1024, 2),
                "gpu_count": len(gpus),
                "gpu_name": gpu.name
            }
            
            logger.debug(f"GPU metrics: {metrics}")
            return metrics
            
        except ImportError:
            logger.warning("GPUtil not installed, GPU metrics unavailable")
            return {
                "gpu_available": False,
                "gpu_percent": 0,
                "gpu_memory_percent": 0,
                "gpu_count": 0
            }
        except Exception as e:
            logger.error(f"Error collecting GPU metrics: {e}")
            return {
                "gpu_available": False,
                "gpu_percent": 0,
                "gpu_memory_percent": 0,
                "gpu_count": 0
            }
    
    def get_disk_metrics(self) -> Dict[str, float]:
        """
        Collect disk I/O metrics.
        
        Returns:
            Dictionary with disk_read_mb_s, disk_write_mb_s, disk_percent
        """
        try:
            import psutil

            disk_io = psutil.disk_io_counters()
            disk_usage = psutil.disk_usage('/')

            metrics = {
                "disk_read_mb": round(disk_io.read_bytes / (1024**2), 2),
                "disk_write_mb": round(disk_io.write_bytes / (1024**2), 2),
                "disk_percent": round(disk_usage.percent, 2),
                "disk_total_gb": round(disk_usage.total / (1024**3), 2),
                "disk_used_gb": round(disk_usage.used / (1024**3), 2),
                "disk_free_gb": round(disk_usage.free / (1024**3), 2)
            }

            logger.debug(f"Disk metrics: {metrics}")
            return metrics

        except ImportError:
            logger.warning("psutil not installed, disk metrics unavailable")
            return {
                "disk_read_mb": 0,
                "disk_write_mb": 0,
                "disk_percent": 0,
                "disk_total_gb": 0,
                "disk_used_gb": 0,
                "disk_free_gb": 0
            }
        except Exception as e:
            logger.error(f"Error collecting disk metrics: {e}")
            return {
                "disk_read_mb": 0,
                "disk_write_mb": 0,
                "disk_percent": 0,
                "disk_total_gb": 0,
                "disk_used_gb": 0,
                "disk_free_gb": 0
            }
    
    def collect_all_metrics(self) -> Dict:
        """Collect all system metrics."""
        timestamp = datetime.now().isoformat()
        
        metrics = {
            "timestamp": timestamp,
            "cpu": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(),
            "gpu": self.get_gpu_metrics(),
            "disk": self.get_disk_metrics()
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_system_health(self) -> Dict[str, str]:
        """
        Determine overall system health status.
        
        Returns:
            Dictionary with health status and thresholds
        """
        cpu = self.get_cpu_metrics()
        memory = self.get_memory_metrics()
        gpu = self.get_gpu_metrics()
        
        status = "Good"
        
        # Simple health scoring
        if cpu["cpu_percent"] > 90 or memory["ram_percent"] > 90:
            status = "Critical"
        elif cpu["cpu_percent"] > 75 or memory["ram_percent"] > 75:
            status = "Warning"
        elif gpu["gpu_available"] and gpu["gpu_percent"] > 85:
            status = "Warning"
        
        return {
            "overall_status": status,
            "cpu_status": "Critical" if cpu["cpu_percent"] > 90 else "Warning" if cpu["cpu_percent"] > 75 else "Good",
            "memory_status": "Critical" if memory["ram_percent"] > 90 else "Warning" if memory["ram_percent"] > 75 else "Good",
            "gpu_status": "N/A" if not gpu["gpu_available"] else "Critical" if gpu["gpu_percent"] > 90 else "Warning" if gpu["gpu_percent"] > 85 else "Good"
        }
