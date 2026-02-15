"""Alert System - Generate alerts for performance issues."""

import logging
from typing import Dict, List, Callable, Optional
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = 1
    WARNING = 2
    CRITICAL = 3


class Alert:
    """Represents a performance alert."""
    
    def __init__(self, level: AlertLevel, message: str, metric: str, value: float, threshold: float):
        """
        Initialize alert.
        
        Args:
            level: Alert level
            message: Alert message
            metric: Metric that triggered the alert
            value: Current metric value
            threshold: Threshold value
        """
        self.level = level
        self.message = message
        self.metric = metric
        self.value = value
        self.threshold = threshold
        self.timestamp = datetime.now().isoformat()
    
    def __str__(self) -> str:
        return f"[{self.level.name}] {self.message}"


class AlertSystem:
    """Manages performance alerts and thresholds."""
    
    def __init__(self):
        """Initialize alert system."""
        self.alerts: List[Alert] = []
        self.thresholds = {
            "latency_warning": 50,      # ms
            "latency_critical": 100,    # ms
            "jitter_warning": 20,       # ms
            "jitter_critical": 50,      # ms
            "packet_loss_warning": 5,   # %
            "packet_loss_critical": 10, # %
            "cpu_warning": 75,          # %
            "cpu_critical": 90,         # %
            "gpu_warning": 80,          # %
            "gpu_critical": 95,         # %
            "fps_warning": 45,          # Below target
            "fps_critical": 30          # Critical
        }
        
        self.alert_handlers: Dict[AlertLevel, List[Callable]] = {
            AlertLevel.INFO: [],
            AlertLevel.WARNING: [],
            AlertLevel.CRITICAL: []
        }
    
    def set_threshold(self, metric: str, value: float):
        """
        Set alert threshold for a metric.
        
        Args:
            metric: Metric name
            value: Threshold value
        """
        self.thresholds[metric] = value
        logger.info(f"Threshold updated - {metric}: {value}")
    
    def check_metrics(self, network_metrics: Dict, system_metrics: Dict) -> List[Alert]:
        """
        Check metrics against thresholds and generate alerts.
        
        Args:
            network_metrics: Network metrics dictionary
            system_metrics: System metrics dictionary
            
        Returns:
            List of triggered alerts
        """
        new_alerts = []
        
        # Check network metrics
        if 'ping_ms' in network_metrics:
            latency = network_metrics['ping_ms']
            if latency > self.thresholds.get("latency_critical", 100):
                alert = Alert(
                    AlertLevel.CRITICAL,
                    f"Critical latency: {latency}ms",
                    "latency",
                    latency,
                    self.thresholds["latency_critical"]
                )
                new_alerts.append(alert)
            elif latency > self.thresholds.get("latency_warning", 50):
                alert = Alert(
                    AlertLevel.WARNING,
                    f"High latency: {latency}ms",
                    "latency",
                    latency,
                    self.thresholds["latency_warning"]
                )
                new_alerts.append(alert)
        
        # Check jitter
        if 'jitter_ms' in network_metrics:
            jitter = network_metrics['jitter_ms']
            if jitter > self.thresholds.get("jitter_critical", 50):
                alert = Alert(
                    AlertLevel.CRITICAL,
                    f"Critical jitter: {jitter}ms",
                    "jitter",
                    jitter,
                    self.thresholds["jitter_critical"]
                )
                new_alerts.append(alert)
            elif jitter > self.thresholds.get("jitter_warning", 20):
                alert = Alert(
                    AlertLevel.WARNING,
                    f"High jitter: {jitter}ms",
                    "jitter",
                    jitter,
                    self.thresholds["jitter_warning"]
                )
                new_alerts.append(alert)
        
        # Check packet loss
        if 'packet_loss_percent' in network_metrics:
            packet_loss = network_metrics['packet_loss_percent']
            if packet_loss > self.thresholds.get("packet_loss_critical", 10):
                alert = Alert(
                    AlertLevel.CRITICAL,
                    f"Critical packet loss: {packet_loss}%",
                    "packet_loss",
                    packet_loss,
                    self.thresholds["packet_loss_critical"]
                )
                new_alerts.append(alert)
            elif packet_loss > self.thresholds.get("packet_loss_warning", 5):
                alert = Alert(
                    AlertLevel.WARNING,
                    f"High packet loss: {packet_loss}%",
                    "packet_loss",
                    packet_loss,
                    self.thresholds["packet_loss_warning"]
                )
                new_alerts.append(alert)
        
        # Check CPU
        if 'cpu_percent' in system_metrics:
            cpu = system_metrics['cpu_percent']
            if cpu > self.thresholds.get("cpu_critical", 90):
                alert = Alert(
                    AlertLevel.CRITICAL,
                    f"Critical CPU usage: {cpu}%",
                    "cpu",
                    cpu,
                    self.thresholds["cpu_critical"]
                )
                new_alerts.append(alert)
            elif cpu > self.thresholds.get("cpu_warning", 75):
                alert = Alert(
                    AlertLevel.WARNING,
                    f"High CPU usage: {cpu}%",
                    "cpu",
                    cpu,
                    self.thresholds["cpu_warning"]
                )
                new_alerts.append(alert)
        
        # Check GPU
        if 'gpu_percent' in system_metrics:
            gpu = system_metrics['gpu_percent']
            if gpu > self.thresholds.get("gpu_critical", 95):
                alert = Alert(
                    AlertLevel.CRITICAL,
                    f"Critical GPU usage: {gpu}%",
                    "gpu",
                    gpu,
                    self.thresholds["gpu_critical"]
                )
                new_alerts.append(alert)
            elif gpu > self.thresholds.get("gpu_warning", 80):
                alert = Alert(
                    AlertLevel.WARNING,
                    f"High GPU usage: {gpu}%",
                    "gpu",
                    gpu,
                    self.thresholds["gpu_warning"]
                )
                new_alerts.append(alert)
        
        # Store and handle new alerts
        self.alerts.extend(new_alerts)
        for alert in new_alerts:
            self._dispatch_alert(alert)
        
        return new_alerts
    
    def _dispatch_alert(self, alert: Alert):
        """
        Dispatch alert to registered handlers.
        
        Args:
            alert: Alert to dispatch
        """
        handlers = self.alert_handlers.get(alert.level, [])
        for handler in handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Error dispatching alert: {e}")
    
    def register_handler(self, level: AlertLevel, handler: Callable):
        """
        Register an alert handler function.
        
        Args:
            level: Alert level to handle
            handler: Callable that takes an Alert object
        """
        self.alert_handlers[level].append(handler)
        logger.info(f"Alert handler registered for {level.name}")
    
    def get_recent_alerts(self, limit: int = 10, level: Optional[AlertLevel] = None) -> List[Alert]:
        """
        Get recent alerts.
        
        Args:
            limit: Maximum number of alerts to return
            level: Filter by alert level (optional)
            
        Returns:
            List of alerts
        """
        if level:
            alerts = [a for a in self.alerts if a.level == level]
        else:
            alerts = self.alerts
        
        return alerts[-limit:]
    
    def clear_alerts(self):
        """Clear all alerts."""
        self.alerts.clear()
        logger.info("All alerts cleared")
