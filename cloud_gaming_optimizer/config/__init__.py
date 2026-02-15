"""Configuration module for Cloud Gaming Performance Optimizer."""

import os
from pathlib import Path
import yaml

CONFIG_DIR = Path(__file__).parent
PROJECT_ROOT = CONFIG_DIR.parent

# Load YAML configuration
CONFIG_FILE = CONFIG_DIR / "settings.yaml"

def load_config():
    """Load configuration from YAML file."""
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    return config

CONFIG = load_config()

# Export commonly used settings
NETWORK_CONFIG = CONFIG.get('network', {})
SYSTEM_CONFIG = CONFIG.get('system', {})
GAMING_CONFIG = CONFIG.get('gaming_settings', {})
OPTIMIZATION_CONFIG = CONFIG.get('optimization', {})
MODEL_CONFIG = CONFIG.get('models', {})
DATA_CONFIG = CONFIG.get('data_collection', {})
LOGGING_CONFIG = CONFIG.get('logging', {})
