"""Unit Tests - Basic test suite."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_collection import NetworkMetricsCollector, SystemMetricsCollector
from src.feature_engineering import FeatureTransformer
from src.optimization_engine import OptimizationRules
from src.monitoring import AlertSystem, PerformanceMonitor


class TestNetworkMetrics:
    """Test network metrics collection."""
    
    def test_metrics_collection(self):
        """Test that metrics are collected."""
        collector = NetworkMetricsCollector()
        metrics = collector.get_ping_metrics()
        
        assert 'ping_ms' in metrics
        assert 'jitter_ms' in metrics
        assert 'packet_loss_percent' in metrics
    
    def test_metrics_are_numeric(self):
        """Test that metrics are numeric values."""
        collector = NetworkMetricsCollector()
        metrics = collector.get_ping_metrics()
        
        assert isinstance(metrics['ping_ms'], (int, float))
        assert isinstance(metrics['jitter_ms'], (int, float))


class TestSystemMetrics:
    """Test system metrics collection."""
    
    def test_cpu_metrics(self):
        """Test CPU metrics collection."""
        collector = SystemMetricsCollector()
        metrics = collector.get_cpu_metrics()
        
        assert 'cpu_percent' in metrics
        assert 0 <= metrics['cpu_percent'] <= 100
    
    def test_memory_metrics(self):
        """Test memory metrics collection."""
        collector = SystemMetricsCollector()
        metrics = collector.get_memory_metrics()
        
        assert 'ram_percent' in metrics
        assert 'ram_used_gb' in metrics
        assert 0 <= metrics['ram_percent'] <= 100


class TestFeatureTransformer:
    """Test feature engineering."""
    
    def test_feature_extraction(self):
        """Test that features are extracted."""
        import pandas as pd
        
        # Create sample data
        df = pd.DataFrame({
            'timestamp': ['2024-01-01 10:00:00', '2024-01-01 10:01:00'],
            'ping_ms': [50, 60],
            'jitter_ms': [5, 8],
            'packet_loss_percent': [0, 1],
            'cpu_percent': [40, 50]
        })
        
        transformer = FeatureTransformer()
        features = transformer.extract_features_from_metrics(df)
        
        assert 'latency_category' in features.columns
        assert len(features) == 2


class TestOptimizationRules:
    """Test optimization rules."""
    
    def test_bitrate_optimization_high_latency(self):
        """Test bitrate reduces with high latency."""
        rules = OptimizationRules()
        
        # High latency should reduce bitrate
        low_latency_bitrate = rules.optimize_bitrate(
            latency_ms=20, packet_loss_percent=0, available_bandwidth_mbps=50
        )
        high_latency_bitrate = rules.optimize_bitrate(
            latency_ms=150, packet_loss_percent=0, available_bandwidth_mbps=50
        )
        
        assert high_latency_bitrate < low_latency_bitrate
    
    def test_resolution_optimization(self):
        """Test resolution selection."""
        rules = OptimizationRules()
        
        # High system load should reduce resolution
        resolution = rules.optimize_resolution(
            bitrate_mbps=50, cpu_load_percent=85, gpu_load_percent=90
        )
        
        assert resolution in ['720p', '1080p', '1440p', '2160p']
    
    def test_fps_optimization(self):
        """Test FPS selection."""
        rules = OptimizationRules()
        
        # High system load should reduce FPS
        fps = rules.optimize_fps(
            cpu_load_percent=80, gpu_load_percent=85, bitrate_mbps=25
        )
        
        assert fps in [30, 60, 120, 144]


class TestAlertSystem:
    """Test alert system."""
    
    def test_alert_generation(self):
        """Test alerts are generated for high latency."""
        alert_system = AlertSystem()
        
        network_metrics = {
            'ping_ms': 150,  # High latency
            'jitter_ms': 10,
            'packet_loss_percent': 0
        }
        
        system_metrics = {
            'cpu_percent': 50
        }
        
        alerts = alert_system.check_metrics(network_metrics, system_metrics)
        
        assert len(alerts) > 0
    
    def test_alert_threshold_setting(self):
        """Test setting alert thresholds."""
        alert_system = AlertSystem()
        alert_system.set_threshold("latency_critical", 200)
        
        assert alert_system.thresholds["latency_critical"] == 200


class TestPerformanceMonitor:
    """Test performance monitoring."""
    
    def test_frame_recording(self):
        """Test recording frame performance."""
        monitor = PerformanceMonitor()
        
        monitor.record_frame(latency_ms=45.5, fps=60, jitter_ms=5)
        
        assert len(monitor.latency_buffer) == 1
        assert len(monitor.fps_buffer) == 1
    
    def test_statistics_calculation(self):
        """Test statistics calculation."""
        monitor = PerformanceMonitor()
        
        # Record multiple frames
        for i in range(5):
            monitor.record_frame(latency_ms=50 + i*5, fps=60)
        
        stats = monitor.get_current_stats()
        
        assert 'avg_latency_ms' in stats
        assert 'avg_fps' in stats
        assert stats['avg_fps'] == 60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
