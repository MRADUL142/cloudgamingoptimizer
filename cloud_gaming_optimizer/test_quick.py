"""Quick Test Script - Run to verify all components work."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("\n" + "="*80)
    print("TEST 1: Module Imports")
    print("="*80)
    
    try:
        print("  ✓ Importing data_collection...", end="")
        from src.data_collection import NetworkMetricsCollector, SystemMetricsCollector, DataLogger
        print(" OK")
        
        print("  ✓ Importing feature_engineering...", end="")
        from src.feature_engineering import FeatureTransformer, FeatureScaler
        print(" OK")
        
        print("  ✓ Importing models...", end="")
        from src.models import ModelManager, ModelTrainer
        print(" OK")
        
        print("  ✓ Importing optimization_engine...", end="")
        from src.optimization_engine import OptimizationRules, GamingOptimizer
        print(" OK")
        
        print("  ✓ Importing monitoring...", end="")
        from src.monitoring import PerformanceMonitor, AlertSystem
        print(" OK")
        
        print("  ✓ Importing ui...", end="")
        from src.ui import CLIDashboard
        print(" OK")
        
        print("\n✅ All imports successful!\n")
        return True
    except ImportError as e:
        print(f" FAILED\n  Error: {e}\n")
        return False


def test_network_metrics():
    """Test network metrics collection."""
    print("="*80)
    print("TEST 2: Network Metrics Collection")
    print("="*80)
    
    try:
        from src.data_collection import NetworkMetricsCollector
        
        collector = NetworkMetricsCollector()
        print("  Collecting network metrics...")
        
        metrics = collector.get_ping_metrics()
        
        print(f"    Latency: {metrics['ping_ms']:.2f} ms")
        print(f"    Jitter: {metrics['jitter_ms']:.2f} ms")
        print(f"    Packet Loss: {metrics['packet_loss_percent']:.2f} %")
        
        assert 'ping_ms' in metrics
        assert 'jitter_ms' in metrics
        
        print("\n✅ Network metrics working!\n")
        return True
    except Exception as e:
        print(f"\n❌ Network metrics failed: {e}\n")
        return False


def test_system_metrics():
    """Test system metrics collection."""
    print("="*80)
    print("TEST 3: System Metrics Collection")
    print("="*80)
    
    try:
        from src.data_collection import SystemMetricsCollector
        
        collector = SystemMetricsCollector()
        print("  Collecting system metrics...")
        
        cpu_metrics = collector.get_cpu_metrics()
        memory_metrics = collector.get_memory_metrics()
        
        print(f"    CPU Usage: {cpu_metrics['cpu_percent']:.1f} %")
        print(f"    RAM Usage: {memory_metrics['ram_percent']:.1f} % ({memory_metrics['ram_used_gb']:.1f}/{memory_metrics['ram_total_gb']:.1f} GB)")
        
        assert 0 <= cpu_metrics['cpu_percent'] <= 100
        assert 0 <= memory_metrics['ram_percent'] <= 100
        
        print("\n✅ System metrics working!\n")
        return True
    except Exception as e:
        print(f"\n❌ System metrics failed: {e}\n")
        return False


def test_optimization_rules():
    """Test optimization rules engine."""
    print("="*80)
    print("TEST 4: Optimization Rules Engine")
    print("="*80)
    
    try:
        from src.optimization_engine import OptimizationRules
        
        rules = OptimizationRules()
        print("  Testing optimization rules...")
        
        # Test case 1: Good conditions
        print("\n  Scenario 1: Good Network Conditions")
        net = {'ping_ms': 40, 'download_mbps': 100, 'jitter_ms': 5, 'packet_loss_percent': 0}
        sys = {'cpu_percent': 50, 'gpu_percent': 60}
        
        settings = rules.generate_recommendations(net, sys, "balanced")
        print(f"    Recommendation: {settings.resolution} @ {settings.fps}fps, {settings.bitrate}Mbps")
        
        # Test case 2: Poor conditions
        print("\n  Scenario 2: Poor Network Conditions")
        net = {'ping_ms': 150, 'download_mbps': 10, 'jitter_ms': 30, 'packet_loss_percent': 8}
        sys = {'cpu_percent': 85, 'gpu_percent': 90}
        
        settings = rules.generate_recommendations(net, sys, "balanced")
        print(f"    Recommendation: {settings.resolution} @ {settings.fps}fps, {settings.bitrate}Mbps")
        
        print("\n✅ Optimization rules working!\n")
        return True
    except Exception as e:
        print(f"\n❌ Optimization rules failed: {e}\n")
        return False


def test_feature_engineering():
    """Test feature engineering."""
    print("="*80)
    print("TEST 5: Feature Engineering")
    print("="*80)
    
    try:
        import pandas as pd
        from src.feature_engineering import FeatureTransformer, FeatureScaler
        
        print("  Creating sample data...")
        df = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=10),
            'ping_ms': [50, 55, 60, 65, 70, 60, 55, 50, 45, 40],
            'jitter_ms': [5, 6, 7, 8, 9, 8, 7, 6, 5, 4],
            'packet_loss_percent': [0, 0, 0.5, 1, 2, 1, 0.5, 0, 0, 0],
            'cpu_percent': [40, 45, 50, 55, 60, 55, 50, 45, 40, 35],
            'ram_percent': [50, 52, 54, 56, 58, 56, 54, 52, 50, 48],
            'gpu_percent': [30, 35, 40, 45, 50, 45, 40, 35, 30, 25]
        })
        
        print("  Extracting features...")
        transformer = FeatureTransformer()
        features = transformer.extract_features_from_metrics(df)
        
        print(f"    Extracted {len(features.columns)} features")
        print(f"    Features: {', '.join(features.columns[:5])}...")
        
        print("  Scaling features...")
        scaler = FeatureScaler()
        scaled = scaler.fit_transform(features)
        
        print(f"    Scaled shape: {scaled.shape}")
        print(f"    Value range: [{scaled.values.min():.2f}, {scaled.values.max():.2f}]")
        
        print("\n✅ Feature engineering working!\n")
        return True
    except Exception as e:
        print(f"\n❌ Feature engineering failed: {e}\n")
        return False


def test_monitoring_and_alerts():
    """Test monitoring and alert system."""
    print("="*80)
    print("TEST 6: Monitoring & Alert System")
    print("="*80)
    
    try:
        from src.monitoring import PerformanceMonitor, AlertSystem, AlertLevel
        
        print("  Testing performance monitor...")
        monitor = PerformanceMonitor()
        
        # Record some frames
        for i in range(5):
            monitor.record_frame(latency_ms=50 + i*10, fps=60)
        
        stats = monitor.get_current_stats()
        print(f"    Avg Latency: {stats['avg_latency_ms']:.2f}ms")
        print(f"    Avg FPS: {stats['avg_fps']:.1f}")
        
        print("\n  Testing alert system...")
        alerts = AlertSystem()
        
        # Trigger high latency alert
        network = {'ping_ms': 150, 'jitter_ms': 30, 'packet_loss_percent': 5}
        system = {'cpu_percent': 95}
        
        triggered = alerts.check_metrics(network, system)
        print(f"    Alerts triggered: {len(triggered)}")
        
        for alert in triggered[:3]:
            print(f"      [{alert.level.name}] {alert.message}")
        
        print("\n✅ Monitoring & alerts working!\n")
        return True
    except Exception as e:
        print(f"\n❌ Monitoring & alerts failed: {e}\n")
        return False


def test_data_logging():
    """Test data logging."""
    print("="*80)
    print("TEST 7: Data Logging")
    print("="*80)
    
    try:
        from src.data_collection import DataLogger
        from datetime import datetime
        
        print("  Creating data logger...")
        logger = DataLogger("data/test_logs")
        
        print("  Logging sample metrics...")
        test_data = {
            'timestamp': datetime.now().isoformat(),
            'ping': {
                'ping_ms': 45.5,
                'jitter_ms': 5.0,
                'packet_loss_percent': 0.0,
                'min_latency_ms': 42.0,
                'max_latency_ms': 48.0
            }
        }
        
        logger.log_network_metrics(test_data)
        
        print("  Loading logged data...")
        df = logger.load_metrics_as_dataframe('network')
        
        print(f"    Rows logged: {len(df)}")
        print(f"    Columns: {', '.join(df.columns[:5].tolist())}...")
        
        print("\n✅ Data logging working!\n")
        return True
    except Exception as e:
        print(f"\n❌ Data logging failed: {e}\n")
        return False


def test_dashboard_rendering():
    """Test CLI dashboard rendering."""
    print("="*80)
    print("TEST 8: CLI Dashboard Rendering")
    print("="*80)
    
    try:
        from src.ui import CLIDashboard
        
        print("  Creating dashboard...")
        dashboard = CLIDashboard()
        
        print("  Rendering sample metrics...")
        
        network_metrics = {
            'ping_ms': 55.0,
            'jitter_ms': 6.0,
            'packet_loss_percent': 0.5,
            'download_mbps': 75.0,
            'upload_mbps': 25.0
        }
        
        system_metrics = {
            'cpu_percent': 45.0,
            'ram_percent': 55.0,
            'gpu_available': True,
            'gpu_percent': 62.0
        }
        
        recommendations = {
            'resolution': '1440p',
            'fps': 120,
            'bitrate_mbps': 30,
            'server_region': 'US-East',
            'priority': 'balanced'
        }
        
        # Print a sample (limited to avoid clutter)
        print("\n  Sample Dashboard Output:")
        print("  " + "-"*76)
        dashboard.print_header()
        dashboard.print_network_metrics(network_metrics)
        dashboard.print_recommendations(recommendations)
        
        print("\n✅ Dashboard rendering working!\n")
        return True
    except Exception as e:
        print(f"\n❌ Dashboard rendering failed: {e}\n")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("CLOUD GAMING OPTIMIZER - QUICK TEST SUITE")
    print("="*80)
    
    results = []
    
    tests = [
        ("Module Imports", test_imports),
        ("Network Metrics", test_network_metrics),
        ("System Metrics", test_system_metrics),
        ("Optimization Rules", test_optimization_rules),
        ("Feature Engineering", test_feature_engineering),
        ("Monitoring & Alerts", test_monitoring_and_alerts),
        ("Data Logging", test_data_logging),
        ("Dashboard Rendering", test_dashboard_rendering),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR in {test_name}: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.\n")
        print("Next steps:")
        print("  1. Run examples: python examples.py")
        print("  2. Run dashboard: python main.py --mode dashboard")
        print("  3. Collect data: python main.py --mode collect --duration 3600")
        print("  4. Read TESTING.md for detailed testing guide")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
