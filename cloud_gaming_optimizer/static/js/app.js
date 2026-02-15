/**
 * Cloud Gaming Optimizer - Dashboard JavaScript
 * Real-time updates and interactive charts
 */

// Configuration
const CONFIG = {
    refreshInterval: 2000, // 2 seconds
    historyLength: 60,     // 60 data points for charts
    apiEndpoints: {
        metrics: '/api/metrics',
        optimize: '/api/optimize',
        alerts: '/api/alerts',
        stats: '/api/stats'
    }
};

// State
let networkHistory = {
    labels: [],
    latency: [],
    jitter: [],
    packetLoss: []
};

let systemHistory = {
    labels: [],
    cpu: [],
    ram: [],
    gpu: []
};

let scoreHistory = {
    labels: [],
    scores: []
};

// Initialize charts when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    startRealTimeUpdates();
});

// Chart instances
let networkChart, systemChart, scoreChart;

/**
 * Initialize all charts
 */
function initializeCharts() {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 300
        },
        plugins: {
            legend: {
                labels: {
                    color: '#94a3b8'
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(51, 65, 85, 0.5)'
                },
                ticks: {
                    color: '#64748b'
                }
            },
            y: {
                grid: {
                    color: 'rgba(51, 65, 85, 0.5)'
                },
                ticks: {
                    color: '#64748b'
                }
            }
        }
    };

    // Network Chart
    const networkCtx = document.getElementById('networkChart').getContext('2d');
    networkChart = new Chart(networkCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Latency (ms)',
                    data: [],
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Jitter (ms)',
                    data: [],
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: chartOptions
    });

    // System Chart
    const systemCtx = document.getElementById('systemChart').getContext('2d');
    systemChart = new Chart(systemCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU %',
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'RAM %',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'GPU %',
                    data: [],
                    borderColor: '#f97316',
                    backgroundColor: 'rgba(249, 115, 22, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: chartOptions
    });

    // Score Chart
    const scoreCtx = document.getElementById('scoreChart').getContext('2d');
    scoreChart = new Chart(scoreCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Performance Score',
                data: [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            ...chartOptions,
            scales: {
                ...chartOptions.scales,
                y: {
                    ...chartOptions.scales.y,
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

/**
 * Start real-time updates
 */
function startRealTimeUpdates() {
    updateAllData();
    setInterval(updateAllData, CONFIG.refreshInterval);
}

/**
 * Update all data from API
 */
async function updateAllData() {
    try {
        const [metricsData, optimizeData, alertsData] = await Promise.all([
            fetch(CONFIG.apiEndpoints.metrics).then(r => r.json()),
            fetch(CONFIG.apiEndpoints.optimize).then(r => r.json()),
            fetch(CONFIG.apiEndpoints.alerts).then(r => r.json())
        ]);

        if (metricsData.success) {
            updateMetricsDisplay(metricsData);
            updateCharts(metricsData);
            updateHealthBanner(metricsData.system_health);
        }

        if (optimizeData.success) {
            updateOptimization(optimizeData);
        }

        if (alertsData.success) {
            updateAlerts(alertsData);
        }

        updateLastUpdateTime();
        setConnectionStatus(true);
    } catch (error) {
        console.error('Error updating data:', error);
        setConnectionStatus(false);
    }
}

/**
 * Update metrics display
 */
function updateMetricsDisplay(data) {
    const network = data.network;
    const system = data.system;

    // Network Metrics
    updateMetricValue('latencyValue', network.ping_ms, 'ms');
    updateMetricValue('jitterValue', network.jitter_ms, 'ms');
    updateMetricValue('packetLossValue', network.packet_loss_percent, '%');

    // Network bars (scale: 0-200ms for latency, 0-100ms for jitter, 0-20% for packet loss)
    updateMetricBar('latencyBar', network.ping_ms, 200);
    updateMetricBar('jitterBar', network.jitter_ms, 100);
    updateMetricBar('packetLossBar', network.packet_loss_percent, 20);

    // System Metrics
    updateMetricValue('cpuValue', system.cpu_percent, '%');
    updateMetricValue('ramValue', system.ram_percent, '%');
    updateMetricValue('gpuValue', system.gpu_available ? system.gpu_percent : '-', '%');
    updateMetricValue('diskValue', system.disk_percent, '%');

    // System bars
    updateMetricBar('cpuBar', system.cpu_percent, 100);
    updateMetricBar('ramBar', system.ram_percent, 100);
    updateMetricBar('gpuBar', system.gpu_percent, 100);
    updateMetricBar('diskBar', system.disk_percent, 100);

    // System details
    document.getElementById('cpuCores').textContent = system.cpu_count || '--';
    document.getElementById('cpuFreq').textContent = system.cpu_freq_ghz || '--';
    document.getElementById('ramUsed').textContent = system.ram_used_gb || '--';
    document.getElementById('ramTotal').textContent = system.ram_total_gb || '--';
    document.getElementById('gpuName').textContent = system.gpu_name || 'N/A';
    document.getElementById('gpuMemory').textContent = system.gpu_memory_percent || '--';
    document.getElementById('diskUsed').textContent = system.disk_used_gb || '--';
    document.getElementById('diskTotal').textContent = system.disk_total_gb || '--';

    // Badges
    updateBadge('cpuBadge', system.cpu_percent);
    updateBadge('ramBadge', system.ram_percent);
    updateBadge('gpuBadge', system.gpu_percent);
    updateBadge('diskBadge', system.disk_percent);
}

/**
 * Update a metric value element
 */
function updateMetricValue(elementId, value, unit) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = typeof value === 'number' ? value.toFixed(1) : value;
    }
}

/**
 * Update a metric bar with color based on value
 */
function updateMetricBar(barId, value, max) {
    const bar = document.getElementById(barId);
    if (bar) {
        const percentage = Math.min((value / max) * 100, 100);
        bar.style.width = percentage + '%';

        // Remove old classes
        bar.classList.remove('warning', 'danger');

        // Add appropriate class based on threshold
        if (percentage >= 80) {
            bar.classList.add('danger');
        } else if (percentage >= 60) {
            bar.classList.add('warning');
        }
    }
}

/**
 * Update badge with color based on value
 */
function updateBadge(badgeId, value) {
    const badge = document.getElementById(badgeId);
    if (badge) {
        badge.textContent = typeof value === 'number' ? value.toFixed(0) + '%' : value;
        badge.classList.remove('warning', 'critical');

        if (value >= 90) {
            badge.classList.add('critical');
        } else if (value >= 75) {
            badge.classList.add('warning');
        }
    }
}

/**
 * Update health banner
 */
function updateHealthBanner(health) {
    const banner = document.getElementById('healthBanner');
    const status = document.getElementById('healthStatus');

    banner.classList.remove('warning', 'critical');

    if (health && health.overall_status) {
        status.textContent = `System Health: ${health.overall_status}`;

        if (health.overall_status === 'Critical') {
            banner.classList.add('critical');
        } else if (health.overall_status === 'Warning') {
            banner.classList.add('warning');
        }
    }
}

/**
 * Update optimization recommendations
 */
function updateOptimization(data) {
    const rec = data.recommendations;

    document.getElementById('recResolution').textContent = rec.resolution || '--';
    document.getElementById('recFps').textContent = rec.fps ? rec.fps + ' FPS' : '--';
    document.getElementById('recBitrate').textContent = rec.bitrate_mbps ? rec.bitrate_mbps + ' Mbps' : '--';
    document.getElementById('recPriority').textContent = rec.priority || '--';
    document.getElementById('optReason').textContent = data.optimization_reason || 'Analyzing...';
}

/**
 * Update alerts display
 */
function updateAlerts(data) {
    const container = document.getElementById('alertsContainer');
    const noAlerts = document.getElementById('noAlerts');
    const alertCount = document.getElementById('alertCount');

    alertCount.textContent = data.alert_count || 0;

    // Clear existing alerts (except no-alerts message)
    const existingAlerts = container.querySelectorAll('.alert-item');
    existingAlerts.forEach(alert => alert.remove());

    if (data.alerts && data.alerts.length > 0) {
        noAlerts.style.display = 'none';

        // Show last 5 alerts
        data.alerts.slice(0, 5).forEach(alert => {
            const alertEl = document.createElement('div');
            alertEl.className = `alert-item ${alert.level.toLowerCase()}`;

            let icon = 'info-circle';
            if (alert.level === 'WARNING') icon = 'exclamation-triangle';
            if (alert.level === 'CRITICAL') icon = 'times-circle';

            alertEl.innerHTML = `
                <i class="fas fa-${icon} alert-icon"></i>
                <div class="alert-content">
                    <div class="alert-message">${alert.message}</div>
                    <div class="alert-meta">${alert.metric} | Threshold: ${alert.threshold}</div>
                </div>
            `;

            container.appendChild(alertEl);
        });
    } else {
        noAlerts.style.display = 'flex';
    }
}

/**
 * Update charts with new data
 */
function updateCharts(data) {
    const now = new Date().toLocaleTimeString();
    const network = data.network;
    const system = data.system;

    // Update network history
    if (networkHistory.labels.length >= CONFIG.historyLength) {
        networkHistory.labels.shift();
        networkHistory.latency.shift();
        networkHistory.jitter.shift();
        networkHistory.packetLoss.shift();
    }
    networkHistory.labels.push(now);
    networkHistory.latency.push(network.ping_ms);
    networkHistory.jitter.push(network.jitter_ms);
    networkHistory.packetLoss.push(network.packet_loss_percent);

    // Update network chart
    networkChart.data.labels = networkHistory.labels;
    networkChart.data.datasets[0].data = networkHistory.latency;
    networkChart.data.datasets[1].data = networkHistory.jitter;
    networkChart.update('none');

    // Update system history
    if (systemHistory.labels.length >= CONFIG.historyLength) {
        systemHistory.labels.shift();
        systemHistory.cpu.shift();
        systemHistory.ram.shift();
        systemHistory.gpu.shift();
    }
    systemHistory.labels.push(now);
    systemHistory.cpu.push(system.cpu_percent);
    systemHistory.ram.push(system.ram_percent);
    systemHistory.gpu.push(system.gpu_percent);

    // Update system chart
    systemChart.data.labels = systemHistory.labels;
    systemChart.data.datasets[0].data = systemHistory.cpu;
    systemChart.data.datasets[1].data = systemHistory.ram;
    systemChart.data.datasets[2].data = systemHistory.gpu;
    systemChart.update('none');

    // Calculate and update performance score
    const score = calculatePerformanceScore(network, system);

    if (scoreHistory.labels.length >= CONFIG.historyLength) {
        scoreHistory.labels.shift();
        scoreHistory.scores.shift();
    }
    scoreHistory.labels.push(now);
    scoreHistory.scores.push(score);

    scoreChart.data.labels = scoreHistory.labels;
    scoreChart.data.datasets[0].data = scoreHistory.scores;
    scoreChart.update('none');
}

/**
 * Calculate performance score based on metrics
 */
function calculatePerformanceScore(network, system) {
    let score = 100;

    // Latency penalty (0-50ms = no penalty, 50-100ms = small, >100ms = large)
    if (network.ping_ms > 50) {
        score -= Math.min((network.ping_ms - 50) * 0.3, 25);
    }

    // Jitter penalty
    if (network.jitter_ms > 10) {
        score -= Math.min((network.jitter_ms - 10) * 0.5, 15);
    }

    // Packet loss penalty
    score -= network.packet_loss_percent * 2;

    // CPU penalty
    if (system.cpu_percent > 70) {
        score -= (system.cpu_percent - 70) * 0.3;
    }

    // RAM penalty
    if (system.ram_percent > 80) {
        score -= (system.ram_percent - 80) * 0.5;
    }

    // GPU penalty (if available)
    if (system.gpu_available && system.gpu_percent > 85) {
        score -= (system.gpu_percent - 85) * 0.4;
    }

    return Math.max(0, Math.min(100, Math.round(score)));
}

/**
 * Update last update time
 */
function updateLastUpdateTime() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = `Last update: ${timeStr}`;
}

/**
 * Set connection status
 */
function setConnectionStatus(connected) {
    const status = document.getElementById('connectionStatus');
    if (connected) {
        status.classList.remove('disconnected');
        status.querySelector('i').classList.add('fa-circle');
        status.querySelector('span:last-child').textContent = 'Connected';
    } else {
        status.classList.add('disconnected');
        status.querySelector('span:last-child').textContent = 'Disconnected';
    }
}
