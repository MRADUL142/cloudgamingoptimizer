"""Feature Scaler - Normalize and scale features for ML models."""

import numpy as np
import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Dict, Tuple
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)


class FeatureScaler:
    """Scales and normalizes features for machine learning."""
    
    def __init__(self, scaler_type: str = "standard"):
        """
        Initialize feature scaler.
        
        Args:
            scaler_type: 'standard' (zero-mean) or 'minmax' (0-1 range)
        """
        self.scaler_type = scaler_type
        
        if scaler_type == "standard":
            self.scaler = StandardScaler()
        elif scaler_type == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaler type: {scaler_type}")
        
        self.fitted = False
        self.feature_names = []
    
    def fit(self, features_df: pd.DataFrame) -> 'FeatureScaler':
        """
        Fit scaler to features.
        
        Args:
            features_df: Training features DataFrame
            
        Returns:
            Self for chaining
        """
        self.scaler.fit(features_df)
        self.feature_names = features_df.columns.tolist()
        self.fitted = True
        logger.info(f"Scaler fitted on {len(features_df)} samples")
        return self
    
    def transform(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform features using fitted scaler.
        
        Args:
            features_df: Features DataFrame to transform
            
        Returns:
            Scaled features DataFrame
        """
        if not self.fitted:
            raise ValueError("Scaler not fitted. Call fit() first.")
        
        scaled_array = self.scaler.transform(features_df)
        return pd.DataFrame(scaled_array, columns=features_df.columns, index=features_df.index)
    
    def fit_transform(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Fit and transform features in one step.
        
        Args:
            features_df: Features DataFrame
            
        Returns:
            Scaled features DataFrame
        """
        scaled_array = self.scaler.fit_transform(features_df)
        self.fitted = True
        self.feature_names = features_df.columns.tolist()
        return pd.DataFrame(scaled_array, columns=features_df.columns, index=features_df.index)
    
    def inverse_transform(self, scaled_df: pd.DataFrame) -> pd.DataFrame:
        """
        Inverse transform scaled features back to original scale.
        
        Args:
            scaled_df: Scaled features DataFrame
            
        Returns:
            Original scale features DataFrame
        """
        if not self.fitted:
            raise ValueError("Scaler not fitted.")
        
        original_array = self.scaler.inverse_transform(scaled_df)
        return pd.DataFrame(original_array, columns=scaled_df.columns, index=scaled_df.index)
    
    def save(self, filepath: str):
        """
        Save fitted scaler to file.
        
        Args:
            filepath: Path to save scaler
        """
        if not self.fitted:
            raise ValueError("Cannot save unfitted scaler.")
        
        joblib.dump(self.scaler, filepath)
        logger.info(f"Scaler saved to {filepath}")
    
    def load(self, filepath: str) -> 'FeatureScaler':
        """
        Load fitted scaler from file.
        
        Args:
            filepath: Path to load scaler from
            
        Returns:
            Self for chaining
        """
        self.scaler = joblib.load(filepath)
        self.fitted = True
        logger.info(f"Scaler loaded from {filepath}")
        return self
    
    def get_scaling_params(self) -> Dict:
        """
        Get scaling parameters (mean/scale or min/max).
        
        Returns:
            Dictionary with scaling parameters
        """
        if not self.fitted:
            raise ValueError("Scaler not fitted.")
        
        if self.scaler_type == "standard":
            return {
                "type": "standard",
                "mean": self.scaler.mean_.tolist(),
                "scale": self.scaler.scale_.tolist(),
                "feature_names": self.feature_names
            }
        elif self.scaler_type == "minmax":
            return {
                "type": "minmax",
                "min": self.scaler.data_min_.tolist(),
                "max": self.scaler.data_max_.tolist(),
                "feature_names": self.feature_names
            }
    
    def scale_single_sample(self, sample: Dict) -> Dict:
        """
        Scale a single sample (e.g., real-time metrics).
        
        Args:
            sample: Dictionary with feature values
            
        Returns:
            Dictionary with scaled values
        """
        if not self.fitted:
            raise ValueError("Scaler not fitted.")
        
        # Create array from sample in feature order
        sample_array = np.array([sample.get(feat, 0) for feat in self.feature_names]).reshape(1, -1)
        
        scaled = self.scaler.transform(sample_array)[0]
        
        return {feat: val for feat, val in zip(self.feature_names, scaled)}
