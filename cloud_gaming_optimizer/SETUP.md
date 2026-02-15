# Cloud Gaming Performance Optimizer - Setup Guide

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda
- 2GB+ RAM
- GPU optional (for GPU monitoring)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd cloud_gaming_optimizer

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Configure Settings

Edit `config/settings.yaml` to customize:

```yaml
# Example: Set latency threshold
network:
  latency_threshold_poor: 100  # ms

# Example: Enable GPU monitoring
system:
  gpu_threshold_high: 80  # %
```

### Step 3: Create Data Directories

Directories are created automatically, but you can pre-create them:

```bash
mkdir -p data/raw_logs data/processed models logs
```

### Step 4: Run the Application

**Dashboard Mode** (recommended for first-time testing):
```bash
python main.py --mode dashboard --interval 2
```

**Collect Data**:
```bash
python main.py --mode collect --duration 3600
```

**Background Service**:
```bash
python service.py --collect-interval 5 --optimize-interval 10
```

### Step 5: Check Results

- **Metrics**: `data/raw_logs/network_metrics.csv` and `system_metrics.csv`
- **Logs**: `logs/optimizer.log`
- **Models**: `models/` directory

## Troubleshooting

### Import Errors
```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Missing Packages
```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade --force-reinstall
```

### Ping Failures (Windows)
Ensure you have permission to use ping. Run as administrator if needed.

### GPU Not Detected
```bash
# Install GPU monitoring
pip install GPUtil
```

## Quick Test

Run the examples to verify installation:
```bash
python examples.py
```

Expected output:
- EXAMPLE 1: Basic optimization recommendations
- EXAMPLE 2: Data collection (5 samples)
- EXAMPLE 3: Monitoring and alerts
- EXAMPLE 4: Quality preferences

## Next Steps

1. **Collect Data**: Run 1-2 hours of data collection during gaming
2. **Explore Data**: Check `data/raw_logs/` for collected metrics
3. **Train Models**: Use collected data to train ML models
4. **Deploy**: Run background service for continuous optimization

## Support

For issues:
1. Check `logs/optimizer.log` for error messages
2. Ensure all dependencies are installed
3. Verify Python version (3.8+)
4. Check file permissions in data/logs/models directories
