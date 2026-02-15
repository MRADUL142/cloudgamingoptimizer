"""Example Usage - Demonstrating the Cloud Gaming Optimizer."""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_collection import NetworkMetricsCollector, SystemMetricsCollector, DataLogger
from feature_engineering import FeatureTransformer, FeatureScaler
from models import ModelManager, ModelTrainer
from optimization_engine import OptimizationRules, GamingOptimizer
from monitoring import PerformanceMonitor, AlertSystem
from ui import CLIDashboard


def example_basic_optimization():
    """Example: Basic optimization without ML."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Rules-Based Optimization")
    print("="*80)
    
    # Create optimizer with rules
    rules = OptimizationRules()
    optimizer = GamingOptimizer(optimization_rules=rules)
    
    # Sample metrics (simulating poor network conditions)
    network_metrics = {
        'ping_ms': 80,
        'jitter_ms': 15,
        'packet_loss_percent': 2,
        'download_mbps': 30
    }
    
    system_metrics = {
        'cpu_percent': 65,
        'gpu_percent': 72,
        'ram_percent': 55
    }
    
    # Get recommendations
    result = optimizer.optimize(network_metrics, system_metrics, quality_preference="balanced")
    
    print("\nInput Metrics:")
    print(f"  Latency: {network_metrics['ping_ms']}ms")
    print(f"  Bandwidth: {network_metrics['download_mbps']}Mbps")
    print(f"  CPU Load: {system_metrics['cpu_percent']}%")
    
    print("\nRecommendations:")
    rec = result['recommendations']
    print(f"  Resolution: {rec['resolution']}")
    print(f"  Target FPS: {rec['fps']}")
    print(f"  Bitrate: {rec['bitrate_mbps']} Mbps")
    print(f"  Priority: {rec['priority']}")


def example_data_collection_and_logging():
    """Example: Collect and log metrics."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Data Collection and Logging")
    print("="*80)
    
    # Initialize collectors
    network = NetworkMetricsCollector()
    system = SystemMetricsCollector()
    logger = DataLogger("data/raw_logs")
    
    print("\nCollecting metrics (5 samples)...")
    
    for i in range(5):
        # Collect metrics
        net = network.collect_all_metrics()
        sys = system.collect_all_metrics()
        
        # Log to files
        logger.log_network_metrics(net)
        logger.log_system_metrics(sys)
        
        print(f"  Sample {i+1}: Latency={net['ping']['ping_ms']:.2f}ms, "
              f"CPU={sys['cpu']['cpu_percent']:.1f}%")
        
        time.sleep(1)
    
    # Show summary
    summary = network.get_metrics_summary()
    print(f"\nNetwork Summary:")
    print(f"  Avg Latency: {summary['avg_latency_ms']:.2f}ms")
    print(f"  Max Latency: {summary['max_latency_ms']:.2f}ms")


def example_monitoring_and_alerts():
    """Example: Performance monitoring and alerts."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Performance Monitoring and Alerts")
    print("="*80)
    
    monitor = PerformanceMonitor()
    alerts = AlertSystem()
    
    # Simulate gaming session with varying performance
    print("\nSimulating gaming session...")
    
    game_data = [
        (50, 60, 5),     # Good conditions
        (45, 60, 4),     # Better
        (120, 45, 25),   # Degraded (high latency)
        (95, 50, 18),    # Recovering
        (55, 58, 6)      # Back to normal
    ]
    
    for latency, fps, jitter in game_data:
        # Record frame
        monitor.record_frame(latency_ms=latency, fps=fps, jitter_ms=jitter)
        
        # Check for alerts
        network_metrics = {
            'ping_ms': latency,
            'jitter_ms': jitter,
            'packet_loss_percent': 0
        }
        
        system_metrics = {
            'cpu_percent': 60,
            'gpu_percent': 70
        }
        
        new_alerts = alerts.check_metrics(network_metrics, system_metrics)
        
        status = "✓" if not new_alerts else "⚠"
        print(f"  {status} Latency={latency}ms, FPS={fps}, Jitter={jitter}ms", end="")
        
        if new_alerts:
            print(f" - {len(new_alerts)} alert(s)")
            for alert in new_alerts:
                print(f"      [{alert.level.name}] {alert.message}")
        else:
            print()
    
    # Show statistics
    stats = monitor.get_current_stats()
    trends = monitor.get_performance_trend()
    
    print(f"\nPerformance Summary:")
    print(f"  Avg Latency: {stats['avg_latency_ms']:.2f}ms")
    print(f"  Avg FPS: {stats['avg_fps']:.1f}")
    print(f"  Latency Trend: {trends.get('latency', 'unknown')}")
    print(f"  FPS Trend: {trends.get('fps', 'unknown')}")


def example_quality_preferences():
    """Example: Different quality preferences."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Quality Preferences")
    print("="*80)
    
    rules = OptimizationRules()
    
    network_metrics = {
        'ping_ms': 60,
        'jitter_ms': 10,
        'packet_loss_percent': 1,
        'download_mbps': 50
    }
    
    system_metrics = {
        'cpu_percent': 50,
        'gpu_percent': 55,
        'ram_percent': 60
    }
    
    preferences = ["quality", "latency", "balanced"]
    
    for pref in preferences:
        settings = rules.generate_recommendations(
            network_metrics, system_metrics, quality_preference=pref
        )
        
        print(f"\n{pref.upper()} Preference:")
        print(f"  Resolution: {settings.resolution}")
        print(f"  FPS: {settings.fps}")
        print(f"  Bitrate: {settings.bitrate} Mbps")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("Cloud Gaming Performance Optimizer - Usage Examples")
    print("="*80)
    
    try:
        example_basic_optimization()
        example_data_collection_and_logging()
        example_monitoring_and_alerts()
        example_quality_preferences()
        
        print("\n" + "="*80)
        print("Examples completed successfully!")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted.")
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
