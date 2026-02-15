"""Cloud Gaming Performance Optimizer - Main Package."""

__version__ = "0.1.0"
__author__ = "Cloud Gaming Team"
__description__ = "ML-powered optimization system for cloud gaming performance"

# Import and expose main submodules for easier access
from . import data_collection
from . import feature_engineering
from . import models
from . import monitoring
from . import optimization_engine
from . import ui

__all__ = [
    'data_collection',
    'feature_engineering',
    'models',
    'monitoring',
    'optimization_engine',
    'ui'
]
