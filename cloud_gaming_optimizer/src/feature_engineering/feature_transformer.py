"""Feature Transformer - Convert raw metrics into engineered features."""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class FeatureTransformer:
    """Transforms raw metrics into ML-ready features."""
    
    def __init__(self):
        """Initialize feature transformer."""
        self.feature_names = []
    
    def extract_features_from_metrics(self, metrics_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from raw metrics DataFrame.
        
        Args:
            metrics_df: DataFrame with timestamp, network, and system metrics
            
        Returns:
            DataFrame with engineered features
        """
        features = pd.DataFrame()
        
        # Timestamp features
        metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'])
        features['hour'] = metrics_df['timestamp'].dt.hour
        features['day_of_week'] = metrics_df['timestamp'].dt.dayofweek
        
        # Network features
        if 'ping_ms' in metrics_df.columns:
            features['latency_category'] = self._categorize_latency(metrics_df['ping_ms'])
            features['jitter_normalized'] = self._normalize_feature(metrics_df.get('jitter_ms', 0), 0, 50)
            features['packet_loss_high'] = (metrics_df.get('packet_loss_percent', 0) > 5).astype(int)
        
        # System features
        if 'cpu_percent' in metrics_df.columns:
            features['cpu_load_normalized'] = self._normalize_feature(metrics_df['cpu_percent'], 0, 100)
            features['cpu_high_load'] = (metrics_df['cpu_percent'] > 80).astype(int)
        
        if 'ram_percent' in metrics_df.columns:
            features['memory_load_normalized'] = self._normalize_feature(metrics_df['ram_percent'], 0, 100)
            features['memory_pressure'] = self._categorize_memory(metrics_df['ram_percent'])
        
        if 'gpu_percent' in metrics_df.columns:
            features['gpu_load_normalized'] = self._normalize_feature(
                metrics_df.get('gpu_percent', 0), 0, 100
            )
            features['gpu_available'] = (metrics_df.get('gpu_percent', 0) > 0).astype(int)
        
        # Rolling statistics (if we have multiple rows)
        if len(metrics_df) > 1:
            if 'ping_ms' in metrics_df.columns:
                features['latency_rolling_mean_3'] = metrics_df['ping_ms'].rolling(3, min_periods=1).mean()
                features['latency_rolling_std_5'] = metrics_df['ping_ms'].rolling(5, min_periods=1).std().fillna(0)
        
        self.feature_names = features.columns.tolist()
        logger.info(f"Extracted {len(self.feature_names)} features")
        
        return features
    
    def _categorize_latency(self, latency_values: pd.Series) -> pd.Series:
        """
        Categorize latency into buckets.
        
        0: Excellent (< 20ms)
        1: Good (20-50ms)
        2: Moderate (50-100ms)
        3: Poor (> 100ms)
        """
        categories = pd.cut(
            latency_values,
            bins=[0, 20, 50, 100, float('inf')],
            labels=[0, 1, 2, 3],
            include_lowest=True
        )
        return categories.astype(int)
    
    def _categorize_memory(self, memory_percent: pd.Series) -> pd.Series:
        """
        Categorize memory pressure.
        
        0: Low (< 50%)
        1: Moderate (50-75%)
        2: High (75-90%)
        3: Critical (> 90%)
        """
        categories = pd.cut(
            memory_percent,
            bins=[0, 50, 75, 90, 100],
            labels=[0, 1, 2, 3],
            include_lowest=True
        )
        return categories.astype(int)
    
    def _normalize_feature(self, values: pd.Series, min_val: float, max_val: float) -> pd.Series:
        """Normalize feature to 0-1 range."""
        if min_val == max_val:
            return pd.Series(0, index=values.index)
        
        normalized = (values - min_val) / (max_val - min_val)
        return normalized.clip(0, 1)
    
    def create_game_context_features(self, game_type: str = "competitive") -> Dict[str, float]:
        """
        Create features based on game type.
        
        Args:
            game_type: 'competitive', 'casual', 'strategy'
            
        Returns:
            Dictionary of context features
        """
        game_features = {
            "competitive": {
                "latency_sensitivity": 1.0,  # High sensitivity to latency
                "fps_requirement": 0.9,       # Needs high FPS
                "bandwidth_requirement": 0.7
            },
            "casual": {
                "latency_sensitivity": 0.5,
                "fps_requirement": 0.6,
                "bandwidth_requirement": 0.5
            },
            "strategy": {
                "latency_sensitivity": 0.3,
                "fps_requirement": 0.5,
                "bandwidth_requirement": 0.4
            }
        }
        
        return game_features.get(game_type, game_features["casual"])
    
    def combine_features(self, features_df: pd.DataFrame, 
                        game_context: Dict[str, float]) -> pd.DataFrame:
        """
        Combine engineered features with game context.
        
        Args:
            features_df: DataFrame with engineered features
            game_context: Game context features
            
        Returns:
            Combined feature DataFrame
        """
        combined = features_df.copy()
        
        for key, value in game_context.items():
            combined[f"game_{key}"] = value
        
        return combined
    
    def get_feature_importance_template(self) -> Dict[str, float]:
        """Get template for feature importance scores."""
        return {
            "latency_category": 0.0,
            "jitter_normalized": 0.0,
            "packet_loss_high": 0.0,
            "cpu_load_normalized": 0.0,
            "memory_load_normalized": 0.0,
            "gpu_load_normalized": 0.0,
            "hour": 0.0,
            "day_of_week": 0.0
        }
