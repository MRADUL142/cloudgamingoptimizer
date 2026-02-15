"""Optimization Rules - Rule-based decision making for gaming settings."""

import logging
from typing import Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class OptimizedSettings:
    """Recommended gaming settings."""
    resolution: str
    fps: int
    bitrate: int
    server_region: str
    priority: str  # "latency", "quality", or "balanced"


class OptimizationRules:
    """Rules-based optimization engine for cloud gaming."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize optimization rules.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
    
    def optimize_bitrate(self, latency_ms: float, packet_loss_percent: float, 
                        available_bandwidth_mbps: float, quality_preference: str = "balanced") -> int:
        """
        Determine optimal bitrate based on network conditions.
        
        Args:
            latency_ms: Network latency in ms
            packet_loss_percent: Packet loss percentage
            available_bandwidth_mbps: Available bandwidth
            quality_preference: 'quality', 'latency', or 'balanced'
            
        Returns:
            Recommended bitrate in Mbps
        """
        bitrate = available_bandwidth_mbps * 0.8  # Use 80% of available bandwidth
        
        # Reduce bitrate if latency is high
        if latency_ms > 100:
            bitrate *= 0.7
        elif latency_ms > 50:
            bitrate *= 0.85
        
        # Reduce bitrate if packet loss is high
        if packet_loss_percent > 10:
            bitrate *= 0.6
        elif packet_loss_percent > 5:
            bitrate *= 0.8
        
        # Apply quality preference
        if quality_preference == "quality":
            bitrate *= 1.2
        elif quality_preference == "latency":
            bitrate *= 0.8
        
        # Cap bitrate to available bandwidth
        bitrate = min(bitrate, available_bandwidth_mbps)
        
        # Round to nearest 5 Mbps
        bitrate = round(bitrate / 5) * 5
        
        logger.info(f"Recommended bitrate: {bitrate} Mbps (latency: {latency_ms}ms, PL: {packet_loss_percent}%)")
        return max(5, int(bitrate))  # Minimum 5 Mbps
    
    def optimize_resolution(self, bitrate_mbps: int, cpu_load_percent: float, 
                           gpu_load_percent: float, quality_preference: str = "balanced") -> str:
        """
        Determine optimal resolution based on available resources.
        
        Args:
            bitrate_mbps: Available bitrate
            cpu_load_percent: CPU load percentage
            gpu_load_percent: GPU load percentage
            quality_preference: 'quality', 'latency', or 'balanced'
            
        Returns:
            Recommended resolution (e.g., '1080p', '1440p')
        """
        resolutions = ['720p', '1080p', '1440p', '2160p']
        
        # High CPU/GPU load -> reduce resolution
        if cpu_load_percent > 85 or gpu_load_percent > 85:
            return '720p'
        elif cpu_load_percent > 70 or gpu_load_percent > 70:
            return '1080p'
        
        # Low bitrate -> reduce resolution
        if bitrate_mbps < 10:
            return '720p'
        elif bitrate_mbps < 20:
            return '1080p'
        elif bitrate_mbps < 40:
            return '1440p'
        
        # Quality preference
        if quality_preference == "quality":
            return '2160p'
        elif quality_preference == "latency":
            return '1080p'
        
        return '1440p'  # Default
    
    def optimize_fps(self, cpu_load_percent: float, gpu_load_percent: float,
                    bitrate_mbps: int, quality_preference: str = "balanced") -> int:
        """
        Determine optimal FPS target.
        
        Args:
            cpu_load_percent: CPU load percentage
            gpu_load_percent: GPU load percentage
            bitrate_mbps: Available bitrate
            quality_preference: 'quality', 'latency', or 'balanced'
            
        Returns:
            Recommended FPS
        """
        fps_options = [30, 60, 120, 144]
        
        # High CPU/GPU load -> reduce FPS
        if cpu_load_percent > 85 or gpu_load_percent > 85:
            return 30
        elif cpu_load_percent > 70 or gpu_load_percent > 70:
            return 60
        
        # Low bitrate -> reduce FPS
        if bitrate_mbps < 15:
            return 30
        elif bitrate_mbps < 30:
            return 60
        elif bitrate_mbps < 50:
            return 120
        
        # Quality preference
        if quality_preference == "quality":
            return 144
        elif quality_preference == "latency":
            return 120
        
        return 120  # Default
    
    def select_server_region(self, latency_to_servers: Dict[str, float]) -> str:
        """
        Select the best server region based on latency.
        
        Args:
            latency_to_servers: Dictionary of server region names to latency values
            
        Returns:
            Recommended server region
        """
        if not latency_to_servers:
            return "default"
        
        best_region = min(latency_to_servers, key=latency_to_servers.get)
        logger.info(f"Selected server region: {best_region} ({latency_to_servers[best_region]}ms)")
        
        return best_region
    
    def generate_recommendations(self, network_metrics: Dict, system_metrics: Dict, 
                                quality_preference: str = "balanced") -> OptimizedSettings:
        """
        Generate complete optimization recommendations.
        
        Args:
            network_metrics: Network metrics dictionary
            system_metrics: System metrics dictionary
            quality_preference: Quality/latency preference
            
        Returns:
            OptimizedSettings object
        """
        # Extract metrics with defaults
        latency = network_metrics.get('ping_ms', 50)
        packet_loss = network_metrics.get('packet_loss_percent', 0)
        bandwidth = network_metrics.get('download_mbps', 50)
        
        cpu_load = system_metrics.get('cpu_percent', 50)
        gpu_load = system_metrics.get('gpu_percent', 50)
        
        # Optimize each setting
        bitrate = self.optimize_bitrate(latency, packet_loss, bandwidth, quality_preference)
        resolution = self.optimize_resolution(bitrate, cpu_load, gpu_load, quality_preference)
        fps = self.optimize_fps(cpu_load, gpu_load, bitrate, quality_preference)
        
        # Determine priority
        if latency > 50:
            priority = "latency"
        elif gpu_load > 75:
            priority = "latency"
        else:
            priority = "quality"
        
        return OptimizedSettings(
            resolution=resolution,
            fps=fps,
            bitrate=bitrate,
            server_region="default",
            priority=priority
        )
    
    def get_optimization_explanation(self, settings: OptimizedSettings, 
                                    network_metrics: Dict, system_metrics: Dict) -> Dict[str, str]:
        """
        Generate explanations for recommended settings.
        
        Args:
            settings: Optimized settings
            network_metrics: Network metrics
            system_metrics: System metrics
            
        Returns:
            Dictionary with explanations for each setting
        """
        explanations = {}
        
        latency = network_metrics.get('ping_ms', 0)
        packet_loss = network_metrics.get('packet_loss_percent', 0)
        cpu_load = system_metrics.get('cpu_percent', 0)
        gpu_load = system_metrics.get('gpu_percent', 0)
        
        # Bitrate explanation
        if latency > 100:
            explanations['bitrate'] = f"High latency ({latency}ms) - reducing bitrate to maintain smoothness"
        elif packet_loss > 5:
            explanations['bitrate'] = f"High packet loss ({packet_loss}%) - reducing bitrate for stability"
        else:
            explanations['bitrate'] = f"Network stable - bitrate optimized for quality"
        
        # Resolution explanation
        if cpu_load > 80 or gpu_load > 80:
            explanations['resolution'] = f"High system load (CPU: {cpu_load}%, GPU: {gpu_load}%) - reducing resolution"
        else:
            explanations['resolution'] = f"System resources available - resolution optimized for quality"
        
        # FPS explanation
        if cpu_load > 80:
            explanations['fps'] = f"CPU utilization high ({cpu_load}%) - reducing target FPS"
        elif gpu_load > 80:
            explanations['fps'] = f"GPU utilization high ({gpu_load}%) - reducing target FPS"
        else:
            explanations['fps'] = f"System resources available - FPS optimized"
        
        return explanations
