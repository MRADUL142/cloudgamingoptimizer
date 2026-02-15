"""Model Trainer - Train and evaluate ML models."""

import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score
)
from typing import Dict, Tuple, Any, Optional
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Trains and evaluates ML models."""
    
    def __init__(self, test_size: float = 0.2, val_size: float = 0.1, random_state: int = 42):
        """
        Initialize model trainer.
        
        Args:
            test_size: Fraction of data for testing (0-1)
            val_size: Fraction of data for validation (0-1)
            random_state: Random seed for reproducibility
        """
        self.test_size = test_size
        self.val_size = val_size
        self.random_state = random_state
        self.training_history: Dict[str, Any] = {}
    
    def split_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
        """
        Split data into train/val/test sets.
        
        Args:
            X: Feature matrix
            y: Target variable
            
        Returns:
            Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        # First split: train + val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state
        )
        
        # Second split: train vs val
        val_size_adjusted = self.val_size / (1 - self.test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp,
            test_size=val_size_adjusted,
            random_state=self.random_state
        )
        
        logger.info(f"Data split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def train_regression_model(self, model: Any, X_train: pd.DataFrame, y_train: pd.Series) -> Any:
        """
        Train a regression model.
        
        Args:
            model: Model instance
            X_train: Training features
            y_train: Training target
            
        Returns:
            Trained model
        """
        try:
            model.fit(X_train, y_train)
            logger.info("Regression model trained successfully")
            return model
        except Exception as e:
            logger.error(f"Error training regression model: {e}")
            raise
    
    def train_classification_model(self, model: Any, X_train: pd.DataFrame, y_train: pd.Series) -> Any:
        """
        Train a classification model.
        
        Args:
            model: Model instance
            X_train: Training features
            y_train: Training target
            
        Returns:
            Trained model
        """
        try:
            model.fit(X_train, y_train)
            logger.info("Classification model trained successfully")
            return model
        except Exception as e:
            logger.error(f"Error training classification model: {e}")
            raise
    
    def evaluate_regression_model(self, model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate regression model performance.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary with metrics
        """
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            "mse": round(mse, 4),
            "rmse": round(rmse, 4),
            "mae": round(mae, 4),
            "r2": round(r2, 4)
        }
        
        logger.info(f"Regression metrics: {metrics}")
        return metrics
    
    def evaluate_classification_model(self, model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate classification model performance.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary with metrics
        """
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        metrics = {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4)
        }
        
        logger.info(f"Classification metrics: {metrics}")
        return metrics
    
    def cross_validate(self, model: Any, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, float]:
        """
        Perform k-fold cross-validation.
        
        Args:
            model: Model instance
            X: Features
            y: Target
            cv: Number of folds
            
        Returns:
            Dictionary with cross-validation scores
        """
        scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
        
        cv_metrics = {
            "mean_cv_score": round(scores.mean(), 4),
            "std_cv_score": round(scores.std(), 4),
            "min_cv_score": round(scores.min(), 4),
            "max_cv_score": round(scores.max(), 4),
            "fold_scores": [round(s, 4) for s in scores]
        }
        
        logger.info(f"Cross-validation metrics: {cv_metrics}")
        return cv_metrics
    
    def hyperparameter_tuning(self, model: Any, X_train: pd.DataFrame, y_train: pd.Series, param_grid: Dict):
        """
        Perform hyperparameter tuning using GridSearchCV.
        
        Args:
            model: Model instance
            X_train: Training features
            y_train: Training target
            param_grid: Dictionary of parameters to tune
            
        Returns:
            Best model and best parameters
        """
        from sklearn.model_selection import GridSearchCV
        
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='r2', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best CV score: {grid_search.best_score_}")
        
        return grid_search.best_estimator_, grid_search.best_params_
    
    def save_training_history(self, history: Dict, filepath: str):
        """
        Save training history to JSON.
        
        Args:
            history: Training history dictionary
            filepath: Path to save
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
        
        logger.info(f"Training history saved: {filepath}")
    
    def load_training_history(self, filepath: str) -> Dict:
        """
        Load training history from JSON.
        
        Args:
            filepath: Path to load from
            
        Returns:
            Training history dictionary
        """
        with open(filepath, 'r') as f:
            history = json.load(f)
        
        logger.info(f"Training history loaded: {filepath}")
        return history
