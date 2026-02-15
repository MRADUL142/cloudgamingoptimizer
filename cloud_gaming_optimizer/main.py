"""Main CLI Entry Point - Cloud Gaming Performance Optimizer."""

import sys
import argparse
import logging
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

# Components are imported lazily inside functions to avoid import-time
# failures when optional dependencies (psutil, pandas, GPUtil, etc.)
# are not available in the execution environment.

NETWORK_CONFIG = {}
SYSTEM_CONFIG = {}
DATA_CONFIG = {"raw_logs_dir": "data/raw_logs"}


def setup_logging(log_file: str = "logs/optimizer.log"):
    """Setup logging configuration."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def run_dashboard_mode(refresh_interval: float = 2):
    """Run CLI dashboard mode."""
    logger = logging.getLogger(__name__)
    logger.info("Starting dashboard mode...")
    
    # Lazy imports to avoid import-time failures for optional packages
    try:
        from src.data_collection.network_metrics import NetworkMetricsCollector
        from src.data_collection.network_metrics import NetworkMetricsCollector
        from src.data_collection.system_metrics import SystemMetricsCollector
        from src.optimization_engine.optimizer import GamingOptimizer
        from src.optimization_engine.optimization_rules import OptimizationRules
        from src.monitoring.performance_monitor import PerformanceMonitor
        from src.monitoring.alert_system import AlertSystem
        from src.ui.cli_dashboard import CLIDashboard
    except Exception as e:
        logger.error(f"Required component import failed: {e}")
        raise

    # Initialize components
    network_collector = NetworkMetricsCollector()
    system_collector = SystemMetricsCollector()
    optimizer = GamingOptimizer(optimization_rules=OptimizationRules())
    monitor = PerformanceMonitor()
    dashboard = CLIDashboard(refresh_interval)
    alert_system = AlertSystem()
    
    try:
        while True:
            # Collect metrics
            net_metrics = network_collector.collect_all_metrics()['ping']
            sys_metrics = system_collector.collect_all_metrics()
            
            # Optimize
            result = optimizer.optimize(net_metrics, sys_metrics)
            
            # Check for alerts
            alerts = alert_system.check_metrics(net_metrics, sys_metrics)
            
            # Record for monitoring
            monitor.record_frame(
                latency_ms=net_metrics.get('ping_ms', 0),
                fps=result['recommendations']['fps']
            )
            
            # Display dashboard
            dashboard.display_full_dashboard(
                network_metrics=net_metrics,
                system_metrics={
                    'cpu_percent': sys_metrics['cpu']['cpu_percent'],
                    'ram_percent': sys_metrics['memory']['ram_percent'],
                    'gpu_percent': sys_metrics['gpu'].get('gpu_percent', 0),
                    'gpu_available': sys_metrics['gpu'].get('gpu_available', False)
                },
                recommendations=result['recommendations'],
                stats=monitor.get_current_stats(),
                alerts=alerts
            )
            
            time.sleep(refresh_interval)
    
    except KeyboardInterrupt:
        print("\n\nDashboard closed.")
        logger.info("Dashboard mode stopped")


def run_collection_mode(duration_seconds: int = 3600):
    """Run data collection mode."""
    logger = logging.getLogger(__name__)
    logger.info(f"Starting data collection mode for {duration_seconds}s...")
    
    try:
        from src.data_collection.network_metrics import NetworkMetricsCollector
        from src.data_collection.system_metrics import SystemMetricsCollector
        from src.data_collection.data_logger import DataLogger
    except Exception as e:
        logger.error(f"Required component import failed: {e}")
        raise

    network_collector = NetworkMetricsCollector()
    system_collector = SystemMetricsCollector()
    data_logger = DataLogger(DATA_CONFIG.get('raw_logs_dir', 'data/raw_logs'))
    
    start_time = time.time()
    collection_count = 0
    
    try:
        while time.time() - start_time < duration_seconds:
            # Collect metrics
            net_metrics = network_collector.collect_all_metrics()
            sys_metrics = system_collector.collect_all_metrics()
            
            # Log to files
            data_logger.log_network_metrics(net_metrics)
            data_logger.log_system_metrics(sys_metrics)
            
            collection_count += 1
            
            if collection_count % 10 == 0:
                print(f"Collected {collection_count} samples...")
                logger.info(f"Collected {collection_count} metric samples")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print(f"\nCollection stopped. Total samples: {collection_count}")
    
    logger.info(f"Data collection completed. {collection_count} samples collected")


def run_optimization_once():
    """Run optimization once and display result."""
    logger = logging.getLogger(__name__)
    logger.info("Running single optimization...")
    
    try:
        from src.data_collection.network_metrics import NetworkMetricsCollector
        from src.data_collection.system_metrics import SystemMetricsCollector
        from src.optimization_engine.optimizer import GamingOptimizer
        from src.optimization_engine.optimization_rules import OptimizationRules
        from src.monitoring.alert_system import AlertSystem
    except Exception as e:
        logger.error(f"Required component import failed: {e}")
        raise

    network_collector = NetworkMetricsCollector()
    system_collector = SystemMetricsCollector()
    optimizer = GamingOptimizer(optimization_rules=OptimizationRules())
    alert_system = AlertSystem()
    
    # Collect metrics
    net_metrics = network_collector.collect_all_metrics()['ping']
    sys_metrics = system_collector.collect_all_metrics()
    
    # Optimize
    result = optimizer.optimize(net_metrics, sys_metrics)
    
    # Check alerts
    alerts = alert_system.check_metrics(net_metrics, sys_metrics)
    
    # Display results
    print("\n" + "="*80)
    print("OPTIMIZATION RESULT")
    print("="*80)
    print(f"\nNetwork Metrics:")
    print(f"  Latency: {net_metrics.get('ping_ms', 0):.2f}ms")
    print(f"  Jitter: {net_metrics.get('jitter_ms', 0):.2f}ms")
    print(f"  Packet Loss: {net_metrics.get('packet_loss_percent', 0):.2f}%")
    
    print(f"\nRecommendations:")
    rec = result['recommendations']
    print(f"  Resolution: {rec['resolution']}")
    print(f"  Target FPS: {rec['fps']}")
    print(f"  Bitrate: {rec['bitrate_mbps']} Mbps")
    print(f"  Priority: {rec['priority']}")
    
    if alerts:
        print(f"\nAlerts ({len(alerts)}):")
        for alert in alerts:
            print(f"  [{alert.level.name}] {alert.message}")
    
    print("\n" + "="*80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Cloud Gaming Performance Optimizer"
    )
    parser.add_argument(
        "--mode",
        choices=["dashboard", "collect", "optimize"],
        default="dashboard",
        help="Operating mode"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Refresh interval for dashboard (seconds)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=3600,
        help="Collection duration (seconds)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    # Try to load configuration values if available
    try:
        from config import NETWORK_CONFIG as _nc, SYSTEM_CONFIG as _sc, DATA_CONFIG as _dc
        NETWORK_CONFIG.update(_nc or {})
        SYSTEM_CONFIG.update(_sc or {})
        DATA_CONFIG.update(_dc or {})
    except Exception:
        logger.warning("Config module unavailable or failed to load; using defaults")

    logger.info(f"Cloud Gaming Performance Optimizer started - Mode: {args.mode}")
    
    try:
        if args.mode == "dashboard":
            run_dashboard_mode(refresh_interval=args.interval)
        elif args.mode == "collect":
            run_collection_mode(duration_seconds=args.duration)
        elif args.mode == "optimize":
            run_optimization_once()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
