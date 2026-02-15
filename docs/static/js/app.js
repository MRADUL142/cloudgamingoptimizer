// Copied JS for GitHub Pages
// Note: The JS expects endpoints like /api/metrics to be available.
// When served via GitHub Pages, those endpoints won't exist. This static
// site is primarily a landing/demo page. You can adapt the endpoints
// to a deployed API if available.

// Minimal placeholder: show static info and no dynamic updates.

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('healthStatus').textContent = 'System Health: Demo (no backend)';
    document.getElementById('latencyValue').textContent = '—';
    document.getElementById('jitterValue').textContent = '—';
    document.getElementById('packetLossValue').textContent = '—';
});
