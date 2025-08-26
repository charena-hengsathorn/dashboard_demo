// Notification System Component
class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.init();
    }

    init() {
        // Check if document.body is available
        if (!document.body) {
            // Retry after a short delay
            setTimeout(() => this.init(), 100);
            return;
        }
        
        // Create notification container
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 400px;
            pointer-events: none;
        `;
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 5000, options = {}) {
        // Ensure container exists
        if (!this.container) {
            this.init();
        }
        
        // Double-check container exists
        if (!this.container) {
            console.warn('Notification container could not be created');
            return null;
        }
        
        const notification = this.createNotification(message, type, options);
        this.container.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        }, 100);

        // Auto remove
        if (duration > 0) {
            setTimeout(() => {
                this.remove(notification);
            }, duration);
        }

        return notification;
    }

    createNotification(message, type, options) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icon = this.getIcon(type);
        const color = this.getColor(type);
        
        notification.style.cssText = `
            background: white;
            border-left: 4px solid ${color};
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            padding: 16px 20px;
            margin-bottom: 10px;
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s ease;
            pointer-events: auto;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            max-width: 400px;
        `;

        notification.innerHTML = `
            <div style="font-size: 20px; color: ${color}; flex-shrink: 0;">${icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; margin-bottom: 4px; color: #2c3e50;">
                    ${this.getTitle(type)}
                </div>
                <div style="color: #7f8c8d; font-size: 14px; line-height: 1.4;">
                    ${message}
                </div>
            </div>
            <button onclick="this.parentElement.remove()" style="
                background: none;
                border: none;
                color: #bdc3c7;
                cursor: pointer;
                font-size: 18px;
                padding: 0;
                flex-shrink: 0;
            ">×</button>
        `;

        return notification;
    }

    getIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️',
            loading: '⏳'
        };
        return icons[type] || icons.info;
    }

    getColor(type) {
        const colors = {
            success: '#27ae60',
            error: '#e74c3c',
            warning: '#f39c12',
            info: '#3498db',
            loading: '#9b59b6'
        };
        return colors[type] || colors.info;
    }

    getTitle(type) {
        const titles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Information',
            loading: 'Loading'
        };
        return titles[type] || 'Information';
    }

    remove(notification) {
        if (!notification) return;
        
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.parentElement.removeChild(notification);
            }
        }, 300);
    }

    // Convenience methods
    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 8000) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration = 6000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }

    loading(message, duration = 0) {
        return this.show(message, 'loading', duration);
    }

    // Clear all notifications
    clear() {
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// Real-time data monitoring
class RealTimeMonitor {
    constructor(dashboardData, notificationSystem) {
        this.dashboardData = dashboardData;
        this.notifications = notificationSystem;
        this.monitoring = false;
        this.thresholds = {
            profit_margin: { min: 5, max: 20 },
            inventory_turnover: { min: 2, max: 10 },
            environmental_score: { min: 50, max: 100 }
        };
    }

    start() {
        this.monitoring = true;
        this.monitor();
        this.notifications.info('Real-time monitoring started');
    }

    stop() {
        this.monitoring = false;
        this.notifications.info('Real-time monitoring stopped');
    }

    monitor() {
        if (!this.monitoring) return;

        // Check profit margin
        const profitMargin = this.dashboardData?.summary_stats?.profit_margin || 0;
        if (profitMargin < this.thresholds.profit_margin.min) {
            this.notifications.warning(`Low profit margin: ${profitMargin.toFixed(1)}%`);
        }

        // Check inventory turnover
        const turnover = this.dashboardData?.advanced_metrics?.inventory_turnover_rate || 0;
        if (turnover < this.thresholds.inventory_turnover.min) {
            this.notifications.warning(`Low inventory turnover: ${turnover.toFixed(1)}`);
        }

        // Check environmental score
        const envScore = this.dashboardData?.environmental_impact?.environmental_score || 0;
        if (envScore < this.thresholds.environmental_score.min) {
            this.notifications.warning(`Low environmental score: ${envScore.toFixed(0)}`);
        }

        // Schedule next check
        setTimeout(() => this.monitor(), 30000); // Check every 30 seconds
    }

    setThresholds(newThresholds) {
        this.thresholds = { ...this.thresholds, ...newThresholds };
    }
}

// Data export utilities
class DataExporter {
    static exportToExcel(data, filename = 'dashboard_data') {
        // Create CSV content
        let csv = '';
        
        // Add summary stats
        csv += 'Summary Statistics\n';
        csv += 'Metric,Value\n';
        Object.entries(data.summary_stats || {}).forEach(([key, value]) => {
            csv += `${key},${value}\n`;
        });
        
        csv += '\nAdvanced Metrics\n';
        csv += 'Metric,Value\n';
        Object.entries(data.advanced_metrics || {}).forEach(([key, value]) => {
            if (typeof value === 'object') {
                csv += `${key},${JSON.stringify(value)}\n`;
            } else {
                csv += `${key},${value}\n`;
            }
        });

        // Create and download file
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${filename}.csv`;
        link.click();
        URL.revokeObjectURL(url);
    }

    static exportToPDF(data, filename = 'dashboard_report') {
        // This would integrate with a PDF library like jsPDF
        console.log('PDF export functionality would be implemented here');
    }

    static exportToJSON(data, filename = 'dashboard_data') {
        const dataStr = JSON.stringify(data, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${filename}.json`;
        link.click();
        URL.revokeObjectURL(url);
    }
}

// Auto-refresh functionality
class AutoRefresh {
    constructor(callback, interval = 60000) { // Default 1 minute
        this.callback = callback;
        this.interval = interval;
        this.timer = null;
        this.enabled = false;
    }

    start() {
        if (this.enabled) return;
        this.enabled = true;
        this.timer = setInterval(this.callback, this.interval);
    }

    stop() {
        if (!this.enabled) return;
        this.enabled = false;
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    setInterval(newInterval) {
        this.interval = newInterval;
        if (this.enabled) {
            this.stop();
            this.start();
        }
    }
}

// Global notification system instance
window.notificationSystem = new NotificationSystem();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        NotificationSystem,
        RealTimeMonitor,
        DataExporter,
        AutoRefresh
    };
}
