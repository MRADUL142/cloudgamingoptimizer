"""Configuration module for Cloud Gaming Performance Optimizer."""

import os
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
PROJECT_ROOT = CONFIG_DIR.parent

# Load YAML configuration if PyYAML is available; otherwise fallback to empty config
CONFIG_FILE = CONFIG_DIR / "settings.yaml"


def _safe_load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except Exception:
        # PyYAML not installed in the runtime (e.g. minimal serverless build).
        # Return an empty config and let callers use sensible defaults.
        return {}

    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                return {}
            return data
    except Exception:
        return {}


CONFIG = _safe_load_yaml(CONFIG_FILE)

# Export commonly used settings with safe defaults
NETWORK_CONFIG = CONFIG.get('network', {})
SYSTEM_CONFIG = CONFIG.get('system', {})
GAMING_CONFIG = CONFIG.get('gaming_settings', {})
OPTIMIZATION_CONFIG = CONFIG.get('optimization', {})
MODEL_CONFIG = CONFIG.get('models', {})
DATA_CONFIG = CONFIG.get('data_collection', {})
LOGGING_CONFIG = CONFIG.get('logging', {})
