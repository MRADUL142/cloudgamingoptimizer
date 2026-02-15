"""Data Logger - Save collected metrics to CSV/JSON."""

import csv
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import pandas as pd

logger = logging.getLogger(__name__)


class DataLogger:
    """Handles logging of collected metrics to files."""
    
    def __init__(self, data_dir: str = "data/raw_logs"):
        """
        Initialize data logger.
        
        Args:
            data_dir: Directory to store raw logs
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.network_csv = self.data_dir / "network_metrics.csv"
        self.system_csv = self.data_dir / "system_metrics.csv"
        self.combined_json = self.data_dir / "metrics.jsonl"
        
        self._initialize_csv_files()
    
    def _initialize_csv_files(self):
        """Create CSV header rows if files don't exist."""
        if not self.network_csv.exists():
            with open(self.network_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'ping_ms', 'jitter_ms', 'packet_loss_percent',
                    'min_latency_ms', 'max_latency_ms'
                ])
        
        if not self.system_csv.exists():
            with open(self.system_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'cpu_percent', 'ram_percent', 'ram_used_gb',
                    'ram_available_gb', 'gpu_percent', 'gpu_memory_percent',
                    'disk_percent'
                ])
    
    def log_network_metrics(self, metrics: Dict):
        """
        Log network metrics to CSV.
        
        Args:
            metrics: Dictionary with ping metrics
        """
        try:
            ping_data = metrics.get('ping', {})
            row = [
                metrics.get('timestamp'),
                ping_data.get('ping_ms', 0),
                ping_data.get('jitter_ms', 0),
                ping_data.get('packet_loss_percent', 0),
                ping_data.get('min_latency_ms', 0),
                ping_data.get('max_latency_ms', 0)
            ]
            
            with open(self.network_csv, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            
            logger.debug("Network metrics logged")
            
        except Exception as e:
            logger.error(f"Error logging network metrics: {e}")
    
    def log_system_metrics(self, metrics: Dict):
        """
        Log system metrics to CSV.
        
        Args:
            metrics: Dictionary with CPU, memory, GPU metrics
        """
        try:
            cpu_data = metrics.get('cpu', {})
            memory_data = metrics.get('memory', {})
            gpu_data = metrics.get('gpu', {})
            
            row = [
                metrics.get('timestamp'),
                cpu_data.get('cpu_percent', 0),
                memory_data.get('ram_percent', 0),
                memory_data.get('ram_used_gb', 0),
                memory_data.get('ram_available_gb', 0),
                gpu_data.get('gpu_percent', 0),
                gpu_data.get('gpu_memory_percent', 0),
                metrics.get('disk', {}).get('disk_percent', 0)
            ]
            
            with open(self.system_csv, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            
            logger.debug("System metrics logged")
            
        except Exception as e:
            logger.error(f"Error logging system metrics: {e}")
    
    def log_combined_metrics(self, network_metrics: Dict, system_metrics: Dict):
        """
        Log combined metrics to JSONL file.
        
        Args:
            network_metrics: Network metrics dictionary
            system_metrics: System metrics dictionary
        """
        try:
            combined = {
                "timestamp": datetime.now().isoformat(),
                "network": network_metrics,
                "system": system_metrics
            }
            
            with open(self.combined_json, 'a') as f:
                f.write(json.dumps(combined) + '\n')
            
            logger.debug("Combined metrics logged")
            
        except Exception as e:
            logger.error(f"Error logging combined metrics: {e}")
    
    def load_metrics_as_dataframe(self, metric_type: str = "system") -> pd.DataFrame:
        """
        Load logged metrics into a pandas DataFrame.
        
        Args:
            metric_type: 'system', 'network', or 'combined'
            
        Returns:
            DataFrame with metrics
        """
        try:
            if metric_type == "system":
                df = pd.read_csv(self.system_csv)
            elif metric_type == "network":
                df = pd.read_csv(self.network_csv)
            elif metric_type == "combined":
                records = []
                with open(self.combined_json, 'r') as f:
                    for line in f:
                        records.append(json.loads(line))
                df = pd.json_normalize(records)
            else:
                raise ValueError(f"Unknown metric type: {metric_type}")
            
            logger.info(f"Loaded {len(df)} {metric_type} records")
            return df
            
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            return pd.DataFrame()
    
    def get_recent_metrics(self, minutes: int = 10, metric_type: str = "system") -> pd.DataFrame:
        """
        Get metrics from the last N minutes.
        
        Args:
            minutes: Number of minutes to look back
            metric_type: Type of metrics to retrieve
            
        Returns:
            DataFrame with recent metrics
        """
        try:
            df = self.load_metrics_as_dataframe(metric_type)
            
            if df.empty:
                return df
            
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            cutoff_time = pd.Timestamp.now() - pd.Timedelta(minutes=minutes)
            
            return df[df['timestamp'] >= cutoff_time]
            
        except Exception as e:
            logger.error(f"Error getting recent metrics: {e}")
            return pd.DataFrame()
    
    def cleanup_old_logs(self, days: int = 30):
        """
        Remove logs older than specified days.
        
        Args:
            days: Number of days to keep
        """
        try:
            cutoff_time = datetime.now() - pd.Timedelta(days=days)
            
            for csv_file in [self.network_csv, self.system_csv]:
                if csv_file.exists():
                    df = pd.read_csv(csv_file)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df[df['timestamp'] >= cutoff_time]
                    df.to_csv(csv_file, index=False)
            
            logger.info(f"Cleaned up logs older than {days} days")
            
        except Exception as e:
            logger.error(f"Error cleaning up old logs: {e}")
