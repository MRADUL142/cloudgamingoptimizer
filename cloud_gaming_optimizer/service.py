"""Background Service - Continuous monitoring and optimization."""

import sys
import argparse
import logging
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_collection import NetworkMetricsCollector, SystemMetricsCollector, DataLogger
from optimization_engine import OptimizationRules, GamingOptimizer
from monitoring import PerformanceMonitor, AlertSystem
from config import DATA_CONFIG


class GamingOptimizationService:
    """Background service for continuous gaming optimization."""
    
    def __init__(self, collect_interval: float = 5, optimize_interval: float = 10):
        """
        Initialize service.
        
        Args:
            collect_interval: Metrics collection interval (seconds)
            optimize_interval: Optimization interval (seconds)
        """
        self.collect_interval = collect_interval
        self.optimize_interval = optimize_interval
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.network_collector = NetworkMetricsCollector()
        self.system_collector = SystemMetricsCollector()
        self.data_logger = DataLogger(DATA_CONFIG['raw_logs_dir'])
        self.optimizer = GamingOptimizer(optimization_rules=OptimizationRules())
        self.monitor = PerformanceMonitor()
        self.alert_system = AlertSystem()
        
        # Setup default alert handler
        from monitoring import AlertLevel
        self.alert_system.register_handler(
            AlertLevel.CRITICAL,
            self._handle_critical_alert
        )
        
        self.running = False
        self.last_optimize = time.time()
    
    def _handle_critical_alert(self, alert):
        """Handle critical alerts."""
        self.logger.critical(f"CRITICAL ALERT: {alert.message}")
        # Could integrate with notification service here
    
    def run(self):
        """Run the service."""
        self.running = True
        self.logger.info("Gaming Optimization Service started")
        
        try:
            while self.running:
                # Collect metrics at regular intervals
                net_metrics = self.network_collector.collect_all_metrics()['ping']
                sys_metrics = self.system_collector.collect_all_metrics()
                
                # Log metrics
                self.data_logger.log_network_metrics(net_metrics)
                self.data_logger.log_system_metrics(sys_metrics)
                
                # Check for alerts
                alerts = self.alert_system.check_metrics(net_metrics, sys_metrics)
                if alerts:
                    self.logger.warning(f"{len(alerts)} alerts triggered")
                
                # Periodic optimization
                if time.time() - self.last_optimize >= self.optimize_interval:
                    result = self.optimizer.optimize(net_metrics, sys_metrics)
                    self.logger.info(f"Optimization: {result['recommendations']['resolution']} @ {result['recommendations']['fps']}fps")
                    self.last_optimize = time.time()
                    
                    # Record for monitoring
                    self.monitor.record_frame(
                        latency_ms=net_metrics.get('ping_ms', 0),
                        fps=result['recommendations']['fps']
                    )
                
                time.sleep(self.collect_interval)
        
        except KeyboardInterrupt:
            self.logger.info("Service interrupted by user")
            self.stop()
        except Exception as e:
            self.logger.error(f"Service error: {e}", exc_info=True)
            self.stop()
    
    def stop(self):
        """Stop the service."""
        self.running = False
        self.logger.info("Gaming Optimization Service stopped")
    
    def get_status(self) -> dict:
        """Get service status."""
        return {
            "running": self.running,
            "uptime": time.time(),
            "last_optimization": self.last_optimize,
            "optimization_count": len(self.optimizer.get_history()),
            "alert_count": len(self.alert_system.get_recent_alerts(limit=100))
        }


def main():
    """Main entry point for service."""
    parser = argparse.ArgumentParser(
        description="Cloud Gaming Optimization Service"
    )
    parser.add_argument(
        "--collect-interval",
        type=float,
        default=5,
        help="Metrics collection interval (seconds)"
    )
    parser.add_argument(
        "--optimize-interval",
        type=float,
        default=10,
        help="Optimization interval (seconds)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_path = Path("logs/service.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Cloud Gaming Optimization Service")
    
    try:
        service = GamingOptimizationService(
            collect_interval=args.collect_interval,
            optimize_interval=args.optimize_interval
        )
        service.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
