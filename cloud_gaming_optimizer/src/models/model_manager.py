"""Model Manager - Load, save, and manage trained models."""

import logging
import joblib
from pathlib import Path
from typing import Dict, Any, Optional
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import pickle

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages ML models for gaming performance prediction."""
    
    # Supported model types
    SUPPORTED_MODELS = {
        "random_forest": RandomForestRegressor,
        "gradient_boosting": GradientBoostingRegressor,
        "xgboost": xgb.XGBRegressor
    }
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize model manager.
        
        Args:
            models_dir: Directory to store models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.models: Dict[str, Any] = {}
    
    def create_model(self, model_name: str, model_type: str, **kwargs) -> Any:
        """
        Create a new model instance.
        
        Args:
            model_name: Name for the model
            model_type: Type of model ('random_forest', 'gradient_boosting', 'xgboost')
            **kwargs: Additional parameters for model initialization
            
        Returns:
            Model instance
        """
        if model_type not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        model_class = self.SUPPORTED_MODELS[model_type]
        
        # Default hyperparameters
        default_params = {
            "random_state": 42,
            "n_jobs": -1
        }
        
        # Update with user parameters
        default_params.update(kwargs)
        
        model = model_class(**default_params)
        self.models[model_name] = model
        
        logger.info(f"Created {model_type} model: {model_name}")
        return model
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """
        Get a model by name.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model instance or None
        """
        return self.models.get(model_name)
    
    def save_model(self, model_name: str, filepath: Optional[str] = None):
        """
        Save a model to disk.
        
        Args:
            model_name: Name of the model
            filepath: Path to save (default: models/{model_name}.pkl)
        """
        if model_name not in self.models:
            raise ValueError(f"Model not found: {model_name}")
        
        if filepath is None:
            filepath = self.models_dir / f"{model_name}.pkl"
        else:
            filepath = Path(filepath)
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.models[model_name], filepath)
        logger.info(f"Model saved: {filepath}")
    
    def load_model(self, model_name: str, filepath: str):
        """
        Load a model from disk.
        
        Args:
            model_name: Name to register model as
            filepath: Path to load model from
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model = joblib.load(filepath)
        self.models[model_name] = model
        logger.info(f"Model loaded: {filepath}")
    
    def save_all_models(self):
        """Save all loaded models."""
        for model_name in self.models:
            self.save_model(model_name)
    
    def load_all_models(self):
        """Load all models from the models directory."""
        for model_file in self.models_dir.glob("*.pkl"):
            model_name = model_file.stem
            self.load_model(model_name, model_file)
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary with model info
        """
        if model_name not in self.models:
            raise ValueError(f"Model not found: {model_name}")
        
        model = self.models[model_name]
        
        return {
            "name": model_name,
            "type": type(model).__name__,
            "params": model.get_params() if hasattr(model, 'get_params') else {},
            "fitted": hasattr(model, 'n_features_in_')
        }
    
    def get_feature_importance(self, model_name: str, feature_names: list = None) -> Dict[str, float]:
        """
        Get feature importance from a trained model.
        
        Args:
            model_name: Name of the model
            feature_names: List of feature names
            
        Returns:
            Dictionary with feature importances
        """
        if model_name not in self.models:
            raise ValueError(f"Model not found: {model_name}")
        
        model = self.models[model_name]
        
        if not hasattr(model, 'feature_importances_'):
            raise ValueError(f"Model {model_name} does not have feature importances")
        
        importances = model.feature_importances_
        
        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(len(importances))]
        
        return dict(zip(feature_names, importances))
    
    def delete_model(self, model_name: str):
        """
        Delete a model from memory.
        
        Args:
            model_name: Name of the model
        """
        if model_name in self.models:
            del self.models[model_name]
            logger.info(f"Model deleted: {model_name}")
    
    def list_models(self) -> list:
        """
        List all loaded models.
        
        Returns:
            List of model names
        """
        return list(self.models.keys())
