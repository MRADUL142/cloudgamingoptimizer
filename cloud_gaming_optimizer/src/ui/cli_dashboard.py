"""CLI Dashboard - Terminal-based dashboard for monitoring."""

import sys
import time
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import curses
except ImportError:
    curses = None


class CLIDashboard:
    """Terminal-based dashboard for real-time monitoring."""
    
    def __init__(self, refresh_interval: float = 2.0):
        """
        Initialize CLI dashboard.
        
        Args:
            refresh_interval: Update interval in seconds
        """
        self.refresh_interval = refresh_interval
        self.running = False
    
    def print_header(self, title: str = "Cloud Gaming Performance Optimizer"):
        """Print dashboard header."""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")
    
    def print_network_metrics(self, metrics: Dict[str, float]):
        """
        Print network metrics.
        
        Args:
            metrics: Network metrics dictionary
        """
        print("NETWORK METRICS")
        print("-" * 80)
        print(f"  Latency:      {metrics.get('ping_ms', 0):.2f} ms")
        print(f"  Jitter:       {metrics.get('jitter_ms', 0):.2f} ms")
        print(f"  Packet Loss:  {metrics.get('packet_loss_percent', 0):.2f} %")
        print(f"  Download:     {metrics.get('download_mbps', 0):.2f} Mbps")
        print(f"  Upload:       {metrics.get('upload_mbps', 0):.2f} Mbps")
        print()
    
    def print_system_metrics(self, metrics: Dict[str, float]):
        """
        Print system metrics.
        
        Args:
            metrics: System metrics dictionary
        """
        print("SYSTEM METRICS")
        print("-" * 80)
        print(f"  CPU:          {metrics.get('cpu_percent', 0):.1f} %")
        print(f"  RAM:          {metrics.get('ram_percent', 0):.1f} % ({metrics.get('ram_used_gb', 0):.1f}/{metrics.get('ram_total_gb', 0):.1f} GB)")
        
        if metrics.get('gpu_available', False):
            print(f"  GPU:          {metrics.get('gpu_percent', 0):.1f} %")
            print(f"  GPU Memory:   {metrics.get('gpu_memory_percent', 0):.1f} % ({metrics.get('gpu_memory_used_gb', 0):.1f}/{metrics.get('gpu_memory_total_gb', 0):.1f} GB)")
        else:
            print(f"  GPU:          Not available")
        
        print(f"  Disk:         {metrics.get('disk_percent', 0):.1f} %")
        print()
    
    def print_recommendations(self, recommendations: Dict[str, Any]):
        """
        Print optimization recommendations.
        
        Args:
            recommendations: Recommendations dictionary
        """
        print("RECOMMENDATIONS")
        print("-" * 80)
        print(f"  Resolution:   {recommendations.get('resolution', 'N/A')}")
        print(f"  Target FPS:   {recommendations.get('fps', 0)}")
        print(f"  Bitrate:      {recommendations.get('bitrate_mbps', 0)} Mbps")
        print(f"  Server:       {recommendations.get('server_region', 'default')}")
        print(f"  Priority:     {recommendations.get('priority', 'balanced')}")
        print()
    
    def print_performance_stats(self, stats: Dict[str, Any]):
        """
        Print performance statistics.
        
        Args:
            stats: Statistics dictionary
        """
        if not stats:
            return
        
        print("PERFORMANCE STATS")
        print("-" * 80)
        
        if 'avg_latency_ms' in stats:
            print(f"  Avg Latency:  {stats['avg_latency_ms']:.2f} ms (min: {stats['min_latency_ms']:.2f}, max: {stats['max_latency_ms']:.2f})")
        if 'avg_fps' in stats:
            print(f"  Avg FPS:      {stats['avg_fps']:.1f} (min: {stats['min_fps']:.1f}, max: {stats['max_fps']:.1f})")
        if 'avg_jitter_ms' in stats:
            print(f"  Avg Jitter:   {stats['avg_jitter_ms']:.2f} ms")
        if 'avg_packet_loss_percent' in stats:
            print(f"  Avg Pkt Loss: {stats['avg_packet_loss_percent']:.2f} %")
        
        print()
    
    def print_alerts(self, alerts: list):
        """
        Print active alerts.
        
        Args:
            alerts: List of alerts
        """
        if not alerts:
            return
        
        print("ALERTS")
        print("-" * 80)
        
        for alert in alerts[-5:]:  # Show last 5 alerts
            print(f"  [{alert.level.name}] {alert.message}")
        
        print()
    
    def display_full_dashboard(self, network_metrics: Dict, system_metrics: Dict,
                              recommendations: Dict, stats: Dict = None, alerts: list = None):
        """
        Display full dashboard.
        
        Args:
            network_metrics: Network metrics
            system_metrics: System metrics
            recommendations: Recommendations
            stats: Performance stats (optional)
            alerts: Alerts list (optional)
        """
        self.print_header()
        self.print_network_metrics(network_metrics)
        self.print_system_metrics(system_metrics)
        self.print_recommendations(recommendations)
        
        if stats:
            self.print_performance_stats(stats)
        
        if alerts:
            self.print_alerts(alerts)
        
        print("-" * 80)
        print(f"  Next update in {self.refresh_interval}s... (Press Ctrl+C to exit)")
    
    def print_simple_status(self, resolution: str, fps: int, bitrate: int, latency: float):
        """
        Print simple status line.
        
        Args:
            resolution: Resolution
            fps: Target FPS
            bitrate: Bitrate in Mbps
            latency: Latency in ms
        """
        print(f"\r[{resolution} | {fps}FPS | {bitrate}Mbps | {latency:.0f}ms]", end='', flush=True)
