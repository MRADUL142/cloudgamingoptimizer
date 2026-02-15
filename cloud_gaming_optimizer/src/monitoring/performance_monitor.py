"""Performance Monitor - Real-time performance tracking."""

import logging
import time
from collections import deque
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitors real-time gaming performance."""
    
    def __init__(self, window_size: int = 300, check_interval: float = 2.0):
        """
        Initialize performance monitor.
        
        Args:
            window_size: Number of samples to keep in history
            check_interval: Interval between checks (seconds)
        """
        self.window_size = window_size
        self.check_interval = check_interval
        
        # Circular buffers for metrics
        self.latency_buffer = deque(maxlen=window_size)
        self.fps_buffer = deque(maxlen=window_size)
        self.jitter_buffer = deque(maxlen=window_size)
        self.packet_loss_buffer = deque(maxlen=window_size)
        
        self.last_check = None
    
    def record_frame(self, latency_ms: float, fps: float, jitter_ms: float = 0.0):
        """
        Record a frame's performance metrics.
        
        Args:
            latency_ms: Frame latency in milliseconds
            fps: Frames per second
            jitter_ms: Jitter in milliseconds
        """
        self.latency_buffer.append(latency_ms)
        self.fps_buffer.append(fps)
        self.jitter_buffer.append(jitter_ms)
        
        self.last_check = datetime.now()
    
    def record_packet_loss(self, loss_percent: float):
        """
        Record packet loss event.
        
        Args:
            loss_percent: Packet loss percentage
        """
        self.packet_loss_buffer.append(loss_percent)
    
    def get_current_stats(self) -> Dict[str, float]:
        """
        Get current performance statistics.
        
        Returns:
            Dictionary with current metrics
        """
        import statistics
        
        stats = {}
        
        if self.latency_buffer:
            stats['avg_latency_ms'] = round(statistics.mean(self.latency_buffer), 2)
            stats['max_latency_ms'] = max(self.latency_buffer)
            stats['min_latency_ms'] = min(self.latency_buffer)
            if len(self.latency_buffer) > 1:
                stats['latency_stdev_ms'] = round(statistics.stdev(self.latency_buffer), 2)
        
        if self.fps_buffer:
            stats['avg_fps'] = round(statistics.mean(self.fps_buffer), 2)
            stats['min_fps'] = min(self.fps_buffer)
            stats['max_fps'] = max(self.fps_buffer)
        
        if self.jitter_buffer:
            stats['avg_jitter_ms'] = round(statistics.mean(self.jitter_buffer), 2)
        
        if self.packet_loss_buffer:
            stats['avg_packet_loss_percent'] = round(statistics.mean(self.packet_loss_buffer), 2)
        
        return stats
    
    def get_performance_trend(self) -> Dict[str, str]:
        """
        Determine performance trend (improving/degrading/stable).
        
        Returns:
            Dictionary with trend for each metric
        """
        trends = {}
        
        if len(self.latency_buffer) >= 3:
            recent = list(self.latency_buffer)[-3:]
            if recent[2] < recent[0] * 0.9:
                trends['latency'] = "improving"
            elif recent[2] > recent[0] * 1.1:
                trends['latency'] = "degrading"
            else:
                trends['latency'] = "stable"
        
        if len(self.fps_buffer) >= 3:
            recent = list(self.fps_buffer)[-3:]
            if recent[2] > recent[0] * 1.1:
                trends['fps'] = "improving"
            elif recent[2] < recent[0] * 0.9:
                trends['fps'] = "degrading"
            else:
                trends['fps'] = "stable"
        
        return trends
    
    def is_degrading(self, threshold_percent: float = 20) -> bool:
        """
        Check if performance is degrading significantly.
        
        Args:
            threshold_percent: Degradation threshold percentage
            
        Returns:
            True if degrading, False otherwise
        """
        if len(self.latency_buffer) < 10:
            return False
        
        first_half = list(self.latency_buffer)[:len(self.latency_buffer)//2]
        second_half = list(self.latency_buffer)[len(self.latency_buffer)//2:]
        
        import statistics
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        degradation = (second_avg - first_avg) / first_avg * 100
        
        return degradation > threshold_percent
    
    def clear_history(self):
        """Clear all recorded metrics."""
        self.latency_buffer.clear()
        self.fps_buffer.clear()
        self.jitter_buffer.clear()
        self.packet_loss_buffer.clear()
        logger.info("Performance monitor history cleared")
