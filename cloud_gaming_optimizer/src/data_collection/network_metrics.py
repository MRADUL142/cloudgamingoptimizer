"""Network Metrics Collection - Ping, latency, jitter, packet loss, bandwidth."""

import subprocess
import time
import json
import logging
import statistics
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class NetworkMetricsCollector:
    """Collects network performance metrics."""
    
    def __init__(self, target_host: str = "8.8.8.8", ping_count: int = 4):
        """
        Initialize network metrics collector.
        
        Args:
            target_host: Host to ping (default: Google DNS)
            ping_count: Number of ping packets to send
        """
        self.target_host = target_host
        self.ping_count = ping_count
        self.metrics_history: List[Dict] = []
    
    def get_ping_metrics(self) -> Dict[str, float]:
        """
        Collect ping metrics (latency, jitter).
        
        Returns:
            Dictionary with ping_ms, jitter_ms, packet_loss_percent
        """
        try:
            # Windows-specific ping command
            cmd = f"ping -n {self.ping_count} {self.target_host}"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            latencies = []
            
            # Parse ping output for latency values
            for line in output.split('\n'):
                if 'time=' in line:
                    try:
                        time_str = line.split('time=')[1].split('ms')[0].strip()
                        latencies.append(float(time_str))
                    except (IndexError, ValueError):
                        continue
            
            if not latencies:
                logger.warning(f"Failed to parse ping output: {output}")
                return {
                    "ping_ms": 0,
                    "jitter_ms": 0,
                    "packet_loss_percent": 100,
                    "min_latency_ms": 0,
                    "max_latency_ms": 0
                }
            
            # Calculate metrics
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            jitter = statistics.stdev(latencies) if len(latencies) > 1 else 0
            packet_loss = 100 - (len(latencies) / self.ping_count * 100)
            
            metrics = {
                "ping_ms": round(avg_latency, 2),
                "jitter_ms": round(jitter, 2),
                "packet_loss_percent": round(packet_loss, 2),
                "min_latency_ms": round(min_latency, 2),
                "max_latency_ms": round(max_latency, 2)
            }
            
            logger.info(f"Ping metrics: {metrics}")
            return metrics
            
        except subprocess.TimeoutExpired:
            logger.error("Ping command timed out")
            return {
                "ping_ms": 0,
                "jitter_ms": 0,
                "packet_loss_percent": 100,
                "min_latency_ms": 0,
                "max_latency_ms": 0
            }
        except Exception as e:
            logger.error(f"Error collecting ping metrics: {e}")
            return {
                "ping_ms": 0,
                "jitter_ms": 0,
                "packet_loss_percent": 100,
                "min_latency_ms": 0,
                "max_latency_ms": 0
            }
    
    def estimate_bandwidth(self) -> Dict[str, float]:
        """
        Estimate bandwidth using speedtest-cli.
        
        Returns:
            Dictionary with download_mbps, upload_mbps
        """
        try:
            import speedtest
            
            st = speedtest.Speedtest()
            st.get_best_server()
            
            download_mbps = st.download() / 1_000_000
            upload_mbps = st.upload() / 1_000_000
            
            metrics = {
                "download_mbps": round(download_mbps, 2),
                "upload_mbps": round(upload_mbps, 2)
            }
            
            logger.info(f"Bandwidth metrics: {metrics}")
            return metrics
            
        except Exception as e:
            logger.warning(f"Bandwidth test failed: {e}")
            return {
                "download_mbps": 0,
                "upload_mbps": 0
            }
    
    def collect_all_metrics(self) -> Dict:
        """Collect all network metrics."""
        timestamp = datetime.now().isoformat()
        
        metrics = {
            "timestamp": timestamp,
            "ping": self.get_ping_metrics()
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_metrics_summary(self) -> Dict:
        """Get summary statistics from collected metrics."""
        if not self.metrics_history:
            return {}
        
        ping_values = [m["ping"]["ping_ms"] for m in self.metrics_history]
        jitter_values = [m["ping"]["jitter_ms"] for m in self.metrics_history]
        
        return {
            "avg_latency_ms": round(statistics.mean(ping_values), 2),
            "max_latency_ms": max(ping_values),
            "min_latency_ms": min(ping_values),
            "latency_stdev_ms": round(statistics.stdev(ping_values), 2) if len(ping_values) > 1 else 0,
            "avg_jitter_ms": round(statistics.mean(jitter_values), 2),
            "collection_count": len(self.metrics_history)
        }
