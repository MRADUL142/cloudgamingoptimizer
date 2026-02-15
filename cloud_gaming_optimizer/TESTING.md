# Testing Guide - Cloud Gaming Performance Optimizer

## Quick Start Testing

### 1. **Run Unit Tests** (5 minutes)
Tests basic functionality of all modules:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_basic.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

**Expected Output:**
- ✓ Test network metrics collection
- ✓ Test system metrics collection
- ✓ Test feature extraction
- ✓ Test optimization rules
- ✓ Test alert system
- ✓ Test performance monitoring

---

## 2. **Run Example Scripts** (10 minutes)

Demonstrates all major features without needing real gaming data:

```bash
python examples.py
```

**Examples Run:**
- **Example 1**: Rules-based optimization with sample data
- **Example 2**: Collect 5 real metrics samples
- **Example 3**: Performance monitoring & alerts
- **Example 4**: Quality preference comparisons

---

## 3. **Test Individual Modules**

### Test Data Collection
```bash
python -c "
from src.data_collection import NetworkMetricsCollector, SystemMetricsCollector

# Test network metrics
network = NetworkMetricsCollector()
print('Network Metrics:', network.get_ping_metrics())

# Test system metrics
system = SystemMetricsCollector()
print('System Metrics:', system.get_cpu_metrics())
"
```

**Expected**: Real latency/CPU values (not errors)

### Test Feature Engineering
```bash
python -c "
from src.feature_engineering import FeatureTransformer, FeatureScaler
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-01', periods=10),
    'ping_ms': [50, 55, 60, 65, 70] * 2,
    'cpu_percent': [40, 45, 50, 55, 60] * 2
})

# Transform features
transformer = FeatureTransformer()
features = transformer.extract_features_from_metrics(df)
print('Extracted features:', features.columns.tolist())

# Scale features
scaler = FeatureScaler()
scaled = scaler.fit_transform(features)
print('Scaled shape:', scaled.shape)
"
```

**Expected**: Feature columns created, data scaled to 0-1 range

### Test Optimization Engine
```bash
python -c "
from src.optimization_engine import OptimizationRules, GamingOptimizer

rules = OptimizationRules()

# Test with different network conditions
test_cases = [
    {'ping_ms': 30, 'download_mbps': 100},   # Excellent
    {'ping_ms': 80, 'download_mbps': 50},    # Good
    {'ping_ms': 150, 'download_mbps': 15},   # Poor
]

for case in test_cases:
    metrics = {
        **case,
        'jitter_ms': 5,
        'packet_loss_percent': 0
    }
    sys_metrics = {'cpu_percent': 50, 'gpu_percent': 60}
    
    result = OptimizationRules().generate_recommendations(metrics, sys_metrics)
    print(f'Latency {case[\"ping_ms\"]}ms -> {result.resolution} {result.fps}fps')
"
```

**Expected**: 
- Poor latency → lower resolution/fps
- Good latency → higher resolution/fps

### Test Monitoring & Alerts
```bash
python -c "
from src.monitoring import PerformanceMonitor, AlertSystem

# Test performance monitor
monitor = PerformanceMonitor()
for i in range(10):
    monitor.record_frame(latency_ms=50 + i*5, fps=60)

stats = monitor.get_current_stats()
print('Avg Latency:', stats['avg_latency_ms'], 'ms')

# Test alert system
alerts = AlertSystem()
network_metrics = {'ping_ms': 150, 'jitter_ms': 30}  # High values
system_metrics = {'cpu_percent': 95}

triggered = alerts.check_metrics(network_metrics, system_metrics)
print(f'Alerts triggered: {len(triggered)}')
for alert in triggered:
    print(f'  - [{alert.level.name}] {alert.message}')
"
```

**Expected**: Latency average, jitter stats, alert detection

### Test Data Logging
```bash
python -c "
from src.data_collection import DataLogger
import pandas as pd

logger = DataLogger('data/test_logs')

# Create sample data
test_data = {
    'timestamp': pd.Timestamp.now().isoformat(),
    'ping': {'ping_ms': 50, 'jitter_ms': 5, 'packet_loss_percent': 0, 'min_latency_ms': 45, 'max_latency_ms': 55}
}

logger.log_network_metrics(test_data)
print('Data logged successfully')

# Load and verify
df = logger.load_metrics_as_dataframe('network')
print('Loaded rows:', len(df))
print('Columns:', df.columns.tolist())
"
```

**Expected**: CSV file created with headers and data

---

## 4. **Test CLI Dashboard**

### Basic Dashboard (2-second updates)
```bash
python main.py --mode dashboard --interval 2
```

**What to check:**
- ✓ Network metrics display (latency, jitter)
- ✓ System metrics display (CPU, GPU, RAM)
- ✓ Real-time recommendations (resolution, FPS, bitrate)
- ✓ Performance stats update
- ✓ No errors in logs/optimizer.log

**Exit**: Press `Ctrl+C`

### Longer Dashboard (slower updates)
```bash
python main.py --mode dashboard --interval 5
```

---

## 5. **Test Data Collection**

### Collect 30 seconds of data
```bash
python main.py --mode collect --duration 30
```

**Check results:**
```bash
# View network metrics
tail -10 data/raw_logs/network_metrics.csv

# View system metrics
tail -10 data/raw_logs/system_metrics.csv

# Count records
wc -l data/raw_logs/network_metrics.csv
```

**Expected**: CSV files with multiple rows of metrics

### Collect 1 hour (background)
```bash
# Windows: Run in PowerShell
Start-Process powershell -ArgumentList "-NoExit", "python main.py --mode collect --duration 3600"
```

---

## 6. **Test Background Service**

Run the continuous optimization service:

```bash
python service.py --collect-interval 5 --optimize-interval 10
```

**Monitor output:**
```bash
# Real-time log
Get-Content logs/service.log -Wait

# Or check log size
ls -la logs/
```

**What happens:**
- Collects metrics every 5 seconds
- Optimizes every 10 seconds
- Logs all activities
- Alerts on performance issues

**Exit**: Press `Ctrl+C`

---

## 7. **Integration Testing** (Simulate Real Usage)

Create a test script that simulates gaming with varying conditions:

```bash
python -c "
import time
from src.data_collection import NetworkMetricsCollector, SystemMetricsCollector, DataLogger
from src.optimization_engine import OptimizationRules, GamingOptimizer
from src.monitoring import AlertSystem, PerformanceMonitor

# Setup
network = NetworkMetricsCollector()
system = SystemMetricsCollector()
logger = DataLogger('data/integration_test')
optimizer = GamingOptimizer(optimization_rules=OptimizationRules())
alerts = AlertSystem()
monitor = PerformanceMonitor()

print('=== INTEGRATION TEST ===\n')

# Simulate 30-second gaming session
for i in range(15):
    # Collect metrics
    net = network.collect_all_metrics()['ping']
    sys = system.collect_all_metrics()
    
    # Log
    logger.log_network_metrics(net)
    logger.log_system_metrics(sys)
    
    # Optimize
    result = optimizer.optimize(net, sys)
    
    # Monitor
    monitor.record_frame(
        latency_ms=net.get('ping_ms', 0),
        fps=result['recommendations']['fps']
    )
    
    # Check alerts
    new_alerts = alerts.check_metrics(net, sys)
    
    # Print status
    print(f'Sample {i+1}:')
    print(f'  Latency: {net.get(\"ping_ms\", 0):.1f}ms')
    print(f'  CPU: {sys[\"cpu\"][\"cpu_percent\"]:.1f}%')
    print(f'  Recommendation: {result[\"recommendations\"][\"resolution\"]} @ {result[\"recommendations\"][\"fps\"]}fps')
    if new_alerts:
        print(f'  Alerts: {len(new_alerts)}')
    print()
    
    time.sleep(2)

print('\nTest completed!')
print('Statistics:', monitor.get_current_stats())
"
```

---

## 8. **Test Configuration Changes**

Edit `config/settings.yaml` and test threshold changes:

```yaml
# Set aggressive thresholds
network:
  latency_threshold_poor: 50  # More sensitive
  jitter_threshold: 10
  packet_loss_threshold: 2

# Run dashboard and see more alerts
```

```bash
python main.py --mode dashboard --interval 2
```

**Expected**: More alerts triggered with lower thresholds

---

## 9. **Validate Output Files**

Check that all output files are created correctly:

```bash
# Check directory structure
ls -R data/ models/ logs/

# Verify CSV files
head -5 data/raw_logs/network_metrics.csv
head -5 data/raw_logs/system_metrics.csv

# Check log file
tail -20 logs/optimizer.log
```

---

## 10. **Performance Testing**

### Memory Usage
```bash
python -c "
import psutil
import os

process = psutil.Process(os.getpid())
print('Initial memory:', process.memory_info().rss / 1024 / 1024, 'MB')

# Import all modules
from src.data_collection import *
from src.feature_engineering import *
from src.models import *
from src.optimization_engine import *
from src.monitoring import *

print('After imports:', process.memory_info().rss / 1024 / 1024, 'MB')
"
```

### Latency
```bash
import time
from src.data_collection import NetworkMetricsCollector

collector = NetworkMetricsCollector()

start = time.time()
metrics = collector.collect_all_metrics()
elapsed = time.time() - start

print(f'Collection took {elapsed*1000:.2f}ms')
```

---

## 11. **Test Edge Cases**

### No GPU Available
The system should handle gracefully:
```bash
python -c "
from src.data_collection import SystemMetricsCollector
collector = SystemMetricsCollector()
metrics = collector.collect_all_metrics()
print('GPU available:', metrics['gpu'].get('gpu_available', False))
print('GPU percent:', metrics['gpu'].get('gpu_percent', 'N/A'))
"
```

### High Latency Scenario
```bash
python -c "
from src.optimization_engine import OptimizationRules

rules = OptimizationRules()

# Extreme high latency
network = {'ping_ms': 500, 'jitter_ms': 100, 'packet_loss_percent': 20, 'download_mbps': 5}
system = {'cpu_percent': 90, 'gpu_percent': 95}

settings = rules.generate_recommendations(network, system, 'balanced')
print('Under extreme conditions:')
print(f'  Resolution: {settings.resolution}')
print(f'  FPS: {settings.fps}')
print(f'  Bitrate: {settings.bitrate}Mbps')
print(f'  Priority: {settings.priority}')
"
```

---

## Test Checklist

- [ ] Unit tests pass (`pytest tests/ -v`)
- [ ] Examples run without errors (`python examples.py`)
- [ ] Dashboard displays metrics correctly
- [ ] Data collection creates CSV files
- [ ] Alerts trigger on high latency/CPU
- [ ] Optimization rules reduce quality on poor conditions
- [ ] Feature engineering scales data correctly
- [ ] Service runs continuously
- [ ] Log files are created
- [ ] No memory leaks after 1 hour of monitoring

---

## Troubleshooting Tests

### Test fails with import errors
```bash
# Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m pytest tests/
```

### Pytest not found
```bash
pip install pytest pytest-cov
```

### Network metrics fail
Ensure you have network connectivity and ping permissions:
```bash
# Windows: Run as Administrator
# Linux/Mac: Check firewall
ping 8.8.8.8
```

### Dashboard shows 0% everywhere
- Dashboard is normal - just shows current CPU/memory
- Run multiple times to get varied data
- Change settings thresholds in config to trigger alerts

---

## Next Testing Steps

After basic testing passes:

1. **Load Testing**: Run for 24+ hours, monitor memory/disk usage
2. **Model Training**: Collect 1+ hours of data, train ML models
3. **Platform Integration**: Test with actual gaming app API calls
4. **User Testing**: Get feedback on recommended settings
5. **Stress Testing**: Simulate poor network conditions
