"""README - Cloud Gaming Performance Optimizer."""

# Cloud Gaming Performance Optimizer

A comprehensive machine learning-powered system to optimize cloud gaming performance in real-time. This project predicts and optimizes network conditions, system resources, and gaming settings for the best possible experience.

## Features

- **Real-time Monitoring**: Continuous tracking of network (latency, jitter, packet loss, bandwidth) and system metrics (CPU, GPU, RAM)
- **ML-Powered Predictions**: Predictive models for latency, frame stability, and performance
- **Intelligent Optimization**: Automatic adjustment of resolution, FPS, bitrate, and server selection
- **Alert System**: Real-time alerts for performance degradation
- **Data Collection Framework**: Easy integration with cloud gaming platforms
- **CLI Dashboard**: Terminal-based monitoring and statistics
- **Web API** (optional): Flask-based REST API for integrations

## Project Structure

```
cloud_gaming_optimizer/
├── src/
│   ├── data_collection/        # Metrics collection
│   │   ├── network_metrics.py  # Ping, latency, jitter, bandwidth
│   │   ├── system_metrics.py   # CPU, GPU, RAM monitoring
│   │   └── data_logger.py      # CSV/JSON logging
│   ├── feature_engineering/    # Feature preparation
│   │   ├── feature_transformer.py
│   │   └── feature_scaler.py
│   ├── models/                 # ML models
│   │   ├── model_manager.py    # Model lifecycle
│   │   └── model_trainer.py    # Training & evaluation
│   ├── optimization_engine/    # Decision making
│   │   ├── optimization_rules.py
│   │   └── optimizer.py
│   ├── monitoring/             # Performance tracking
│   │   ├── performance_monitor.py
│   │   └── alert_system.py
│   └── ui/                     # User interfaces
│       └── cli_dashboard.py
├── config/
│   ├── settings.yaml           # Configuration
│   └── __init__.py
├── data/
│   ├── raw_logs/               # Collected metrics
│   └── processed/              # Processed features
├── models/                     # Trained models
├── logs/                       # Application logs
├── tests/                      # Unit tests
├── main.py                     # CLI entry point
├── service.py                  # Background service
└── requirements.txt            # Dependencies
```

## Quick Start

### 1. Installation

```bash
# Clone or navigate to project directory
cd cloud_gaming_optimizer

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit `config/settings.yaml` to customize:
- Network thresholds (latency, jitter, packet loss)
- System resource limits (CPU, GPU, RAM)
- Gaming settings (resolutions, FPS options, bitrates)
- Optimization rules and priorities

### 3. Basic Usage

#### Data Collection
```python
from src.data_collection import NetworkMetricsCollector, SystemMetricsCollector, DataLogger

# Collect metrics
network = NetworkMetricsCollector()
system = SystemMetricsCollector()
logger = DataLogger("data/raw_logs")

# Get metrics
net_metrics = network.collect_all_metrics()
sys_metrics = system.collect_all_metrics()

# Log to CSV
logger.log_network_metrics(net_metrics)
logger.log_system_metrics(sys_metrics)
```

#### Feature Engineering
```python
from src.feature_engineering import FeatureTransformer, FeatureScaler
import pandas as pd

# Load metrics
df = logger.load_metrics_as_dataframe("system")

# Transform features
transformer = FeatureTransformer()
features = transformer.extract_features_from_metrics(df)

# Scale features
scaler = FeatureScaler("standard")
scaled_features = scaler.fit_transform(features)
```

#### Model Training
```python
from src.models import ModelManager, ModelTrainer

# Create and train model
manager = ModelManager()
model = manager.create_model("latency_predictor", "random_forest", n_estimators=100)

trainer = ModelTrainer()
X_train, X_val, X_test, y_train, y_val, y_test = trainer.split_data(features, target)

trained_model = trainer.train_regression_model(model, X_train, y_train)
metrics = trainer.evaluate_regression_model(trained_model, X_test, y_test)

# Save model
manager.save_model("latency_predictor")
```

#### Optimization
```python
from src.optimization_engine import OptimizationRules, GamingOptimizer
from src.monitoring import PerformanceMonitor, AlertSystem

# Create optimizer
rules = OptimizationRules()
optimizer = GamingOptimizer(optimization_rules=rules)

# Get real-time metrics
network_metrics = network.collect_all_metrics()['ping']
system_metrics = system.collect_all_metrics()['cpu']

# Optimize
result = optimizer.optimize(network_metrics, system_metrics, quality_preference="balanced")
print(f"Recommended settings: {result['recommendations']}")

# Monitor performance
monitor = PerformanceMonitor()
monitor.record_frame(latency_ms=45.5, fps=60)

# Alert on issues
alert_system = AlertSystem()
new_alerts = alert_system.check_metrics(network_metrics, system_metrics)
if new_alerts:
    for alert in new_alerts:
        print(f"Alert: {alert}")
```

#### CLI Dashboard
```python
from src.ui import CLIDashboard

dashboard = CLIDashboard()
dashboard.display_full_dashboard(
    network_metrics=network_metrics,
    system_metrics=system_metrics,
    recommendations=result['recommendations'],
    stats=monitor.get_current_stats()
)
```

## Configuration Guide

### Network Settings
- `latency_threshold_poor`: Latency considered "poor" (default: 100ms)
- `latency_threshold_moderate`: Latency considered "moderate" (default: 50ms)
- `packet_loss_threshold`: Critical packet loss % (default: 5%)
- `jitter_threshold`: Critical jitter (default: 20ms)

### System Settings
- `cpu_threshold_high`: High CPU load % (default: 85%)
- `cpu_threshold_critical`: Critical CPU load % (default: 95%)
- `gpu_threshold_high`: High GPU load % (default: 80%)
- `ram_threshold_high`: High RAM usage % (default: 80%)

### Optimization Rules
The optimizer automatically adjusts:
- **Resolution**: 720p → 1080p → 1440p → 2160p
- **FPS**: 30 → 60 → 120 → 144 fps
- **Bitrate**: 5 → 10 → 25 → 50 Mbps

Based on:
- Network latency and packet loss
- CPU/GPU utilization
- Available bandwidth
- User quality preferences

## Running the Service

### CLI Dashboard
```bash
python main.py --mode dashboard --interval 2
```

### Background Service
```bash
python service.py --collect-interval 5 --optimize-interval 10
```

### Data Collection Only
```bash
python main.py --mode collect --duration 3600
```

## Model Training

### Prepare Data
```bash
# Collect data from gaming sessions
python main.py --mode collect --duration 7200 --output data/raw_logs
```

### Train Models
```bash
# Feature engineering
python -c "from scripts.train import prepare_features; prepare_features('data/raw_logs', 'data/processed')"

# Train and evaluate
python -c "from scripts.train import train_models; train_models('data/processed', 'models')"
```

## Supported Cloud Gaming Platforms

- NVIDIA GeForce NOW
- Xbox Cloud Gaming
- PlayStation Now
- Amazon Luna
- Google Stadia (historical)

Currently uses generic network/system optimization. Can be extended with platform-specific APIs.

## Performance Metrics

The optimizer tracks:
- **Latency**: Frame input lag and network RTT
- **FPS Stability**: Frame rate consistency
- **Jitter**: Latency variance
- **Packet Loss**: Network reliability
- **CPU/GPU Load**: System resource usage
- **Smoothness Score**: Subjective quality metric

## Extensibility

### Adding New Metrics
Create a new collector in `src/data_collection/`:
```python
class CustomMetricsCollector:
    def collect_all_metrics(self) -> Dict:
        # Implementation
        pass
```

### Adding New Models
```python
manager = ModelManager()
model = manager.create_model("custom_model", "xgboost", **hyperparams)
```

### Custom Optimization Rules
```python
class CustomRules(OptimizationRules):
    def optimize_resolution(self, **kwargs) -> str:
        # Custom logic
        pass
```

## Future Enhancements

- [ ] Reinforcement Learning agent for dynamic adjustments
- [ ] Web dashboard with real-time visualization
- [ ] Integration with streaming platforms (Twitch, YouTube)
- [ ] Mobile app for remote monitoring
- [ ] Cloud deployment support (AWS, Azure, GCP)
- [ ] Platform-specific API integrations
- [ ] User feedback learning loop
- [ ] Multi-session load balancing

## Contributing

Contributions are welcome! Areas to improve:
- Platform-specific optimizations
- Additional ML models
- Web UI implementation
- Test coverage

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on the project repository.
