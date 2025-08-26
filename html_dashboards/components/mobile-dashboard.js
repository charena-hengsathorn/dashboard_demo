// Mobile Dashboard Component
class MobileDashboard {
    constructor() {
        this.isMobile = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.init();
    }

    init() {
        this.checkDevice();
        this.setupEventListeners();
        this.optimizeForMobile();
    }

    checkDevice() {
        this.isMobile = window.innerWidth <= 768 || 
                       /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    setupEventListeners() {
        // Touch gestures for mobile
        if (this.isMobile) {
            this.setupTouchGestures();
        }

        // Resize handler
        window.addEventListener('resize', () => {
            const wasMobile = this.isMobile;
            this.checkDevice();
            if (wasMobile !== this.isMobile) {
                this.optimizeForMobile();
            }
        });
    }

    setupTouchGestures() {
        // Swipe to refresh
        let touchStartY = 0;
        let touchEndY = 0;

        document.addEventListener('touchstart', (e) => {
            touchStartY = e.changedTouches[0].screenY;
        });

        document.addEventListener('touchend', (e) => {
            touchEndY = e.changedTouches[0].screenY;
            this.handleSwipeGesture(touchStartY, touchEndY);
        });

        // Swipe navigation
        let touchStartX = 0;
        let touchEndX = 0;

        document.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });

        document.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleHorizontalSwipe(touchStartX, touchEndX);
        });
    }

    handleSwipeGesture(startY, endY) {
        const swipeDistance = startY - endY;
        const minSwipeDistance = 100;

        if (swipeDistance > minSwipeDistance) {
            // Swipe up - refresh data
            this.refreshData();
        }
    }

    handleHorizontalSwipe(startX, endX) {
        const swipeDistance = startX - endX;
        const minSwipeDistance = 50;

        if (Math.abs(swipeDistance) > minSwipeDistance) {
            if (swipeDistance > 0) {
                // Swipe left - next section
                this.navigateToNextSection();
            } else {
                // Swipe right - previous section
                this.navigateToPreviousSection();
            }
        }
    }

    optimizeForMobile() {
        if (this.isMobile) {
            this.applyMobileStyles();
            this.createMobileNavigation();
            this.optimizeCharts();
            this.createTouchFriendlyControls();
        } else {
            this.removeMobileOptimizations();
        }
    }

    applyMobileStyles() {
        // Add mobile-specific CSS
        const mobileStyles = document.createElement('style');
        mobileStyles.id = 'mobile-styles';
        mobileStyles.textContent = `
            @media (max-width: 768px) {
                .container {
                    flex-direction: column !important;
                }
                
                .sidebar {
                    width: 100% !important;
                    min-height: auto !important;
                    position: fixed;
                    top: 0;
                    left: -100%;
                    z-index: 1000;
                    transition: left 0.3s ease;
                }
                
                .sidebar.open {
                    left: 0;
                }
                
                .main-content {
                    margin-left: 0 !important;
                    padding-top: 60px;
                }
                
                .mobile-header {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background: #2c3e50;
                    color: white;
                    padding: 15px;
                    z-index: 999;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .mobile-menu-btn {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 24px;
                    cursor: pointer;
                }
                
                .stats-bar {
                    grid-template-columns: 1fr !important;
                    gap: 10px !important;
                    padding: 10px !important;
                }
                
                .stat-card {
                    padding: 15px !important;
                }
                
                .charts-grid {
                    grid-template-columns: 1fr !important;
                    gap: 15px !important;
                }
                
                .chart-card {
                    padding: 15px !important;
                }
                
                .chart-container {
                    height: 250px !important;
                }
                
                .analytics-grid {
                    grid-template-columns: 1fr !important;
                    gap: 15px !important;
                }
                
                .filter-section {
                    flex-direction: column !important;
                    gap: 10px !important;
                    padding: 15px !important;
                }
                
                .filter-group {
                    width: 100% !important;
                }
                
                .filter-group select,
                .filter-group input {
                    width: 100% !important;
                    min-width: auto !important;
                }
                
                .btn {
                    padding: 12px 20px !important;
                    font-size: 16px !important;
                    min-height: 44px !important;
                }
                
                .environmental-grid,
                .market-grid,
                .forecast-grid {
                    grid-template-columns: 1fr !important;
                    gap: 10px !important;
                }
                
                .environmental-card,
                .market-card,
                .forecast-card {
                    padding: 15px !important;
                }
                
                .mobile-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.5);
                    z-index: 999;
                    display: none;
                }
                
                .mobile-overlay.open {
                    display: block;
                }
            }
        `;
        
        if (!document.getElementById('mobile-styles')) {
            document.head.appendChild(mobileStyles);
        }
    }

    createMobileNavigation() {
        // Create mobile header
        const mobileHeader = document.createElement('div');
        mobileHeader.className = 'mobile-header';
        mobileHeader.innerHTML = `
            <button class="mobile-menu-btn" onclick="mobileDashboard.toggleSidebar()">
                <i class="fas fa-bars"></i>
            </button>
            <h1 style="font-size: 18px; margin: 0;">Dashboard</h1>
            <button class="mobile-menu-btn" onclick="mobileDashboard.refreshData()">
                <i class="fas fa-sync-alt"></i>
            </button>
        `;
        
        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'mobile-overlay';
        overlay.onclick = () => this.toggleSidebar();
        
        document.body.appendChild(mobileHeader);
        document.body.appendChild(overlay);
    }

    optimizeCharts() {
        // Optimize Chart.js for mobile
        if (typeof Chart !== 'undefined') {
            Chart.defaults.font.size = 12;
            Chart.defaults.font.family = 'system-ui, -apple-system, sans-serif';
            
            // Reduce animation duration for better performance
            Chart.defaults.animation.duration = 500;
        }
    }

    createTouchFriendlyControls() {
        // Make buttons and controls touch-friendly
        const buttons = document.querySelectorAll('.btn, button, select, input');
        buttons.forEach(button => {
            button.style.minHeight = '44px';
            button.style.fontSize = '16px';
        });
    }

    removeMobileOptimizations() {
        // Remove mobile-specific elements
        const mobileHeader = document.querySelector('.mobile-header');
        const overlay = document.querySelector('.mobile-overlay');
        const mobileStyles = document.getElementById('mobile-styles');
        
        if (mobileHeader) mobileHeader.remove();
        if (overlay) overlay.remove();
        if (mobileStyles) mobileStyles.remove();
        
        // Reset sidebar
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.left = '0';
            sidebar.classList.remove('open');
        }
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.mobile-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
        }
    }

    refreshData() {
        // Trigger data refresh
        if (window.loadDashboardData) {
            window.loadDashboardData();
            if (window.notificationSystem) {
                window.notificationSystem.success('Data refreshed!');
            }
        }
    }

    navigateToNextSection() {
        // Navigate to next dashboard section
        const sections = document.querySelectorAll('.dashboard-section, .environmental-section, .market-section, .predictive-section');
        const currentSection = this.getCurrentSection(sections);
        
        if (currentSection && currentSection.nextElementSibling) {
            currentSection.nextElementSibling.scrollIntoView({ behavior: 'smooth' });
        }
    }

    navigateToPreviousSection() {
        // Navigate to previous dashboard section
        const sections = document.querySelectorAll('.dashboard-section, .environmental-section, .market-section, .predictive-section');
        const currentSection = this.getCurrentSection(sections);
        
        if (currentSection && currentSection.previousElementSibling) {
            currentSection.previousElementSibling.scrollIntoView({ behavior: 'smooth' });
        }
    }

    getCurrentSection(sections) {
        const scrollTop = window.pageYOffset;
        const windowHeight = window.innerHeight;
        
        for (let section of sections) {
            const rect = section.getBoundingClientRect();
            if (rect.top <= windowHeight / 2 && rect.bottom >= windowHeight / 2) {
                return section;
            }
        }
        
        return sections[0];
    }

    // Mobile-specific chart optimizations
    optimizeChartForMobile(chart) {
        if (!this.isMobile || !chart) return;
        
        // Reduce data points for better performance
        if (chart.data.labels && chart.data.labels.length > 10) {
            const step = Math.ceil(chart.data.labels.length / 10);
            chart.data.labels = chart.data.labels.filter((_, index) => index % step === 0);
            chart.data.datasets.forEach(dataset => {
                dataset.data = dataset.data.filter((_, index) => index % step === 0);
            });
        }
        
        // Update chart options for mobile
        chart.options.responsive = true;
        chart.options.maintainAspectRatio = false;
        chart.options.plugins.legend.position = 'bottom';
        chart.options.plugins.legend.labels.boxWidth = 12;
        chart.options.plugins.legend.labels.padding = 8;
        
        chart.update();
    }

    // Create mobile-friendly data table
    createMobileTable(data, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        if (this.isMobile) {
            // Create card-based layout for mobile
            container.innerHTML = '';
            data.forEach((item, index) => {
                const card = document.createElement('div');
                card.style.cssText = `
                    background: white;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                `;
                
                card.innerHTML = `
                    <div style="font-weight: 600; margin-bottom: 8px;">Item ${index + 1}</div>
                    ${Object.entries(item).map(([key, value]) => `
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="color: #7f8c8d;">${key}:</span>
                            <span style="font-weight: 500;">${value}</span>
                        </div>
                    `).join('')}
                `;
                
                container.appendChild(card);
            });
        } else {
            // Create regular table for desktop
            // This would be handled by the existing table creation logic
        }
    }

    // Mobile gesture helpers
    enablePullToRefresh(callback) {
        if (!this.isMobile) return;
        
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        const threshold = 80;
        
        document.addEventListener('touchstart', (e) => {
            if (window.pageYOffset === 0) {
                startY = e.touches[0].clientY;
            }
        });
        
        document.addEventListener('touchmove', (e) => {
            if (startY > 0) {
                currentY = e.touches[0].clientY;
                pullDistance = currentY - startY;
                
                if (pullDistance > 0 && pullDistance < threshold) {
                    // Show pull indicator
                    this.showPullIndicator(pullDistance);
                }
            }
        });
        
        document.addEventListener('touchend', (e) => {
            if (pullDistance > threshold) {
                callback();
            }
            this.hidePullIndicator();
            startY = 0;
            pullDistance = 0;
        });
    }

    showPullIndicator(distance) {
        // Create or update pull-to-refresh indicator
        let indicator = document.getElementById('pull-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'pull-indicator';
            indicator.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: #3498db;
                color: white;
                text-align: center;
                padding: 10px;
                z-index: 1001;
                transform: translateY(-100%);
                transition: transform 0.3s ease;
            `;
            document.body.appendChild(indicator);
        }
        
        indicator.textContent = `Pull to refresh (${Math.round(distance)}px)`;
        indicator.style.transform = `translateY(${Math.min(distance, 60)}px)`;
    }

    hidePullIndicator() {
        const indicator = document.getElementById('pull-indicator');
        if (indicator) {
            indicator.style.transform = 'translateY(-100%)';
        }
    }
}

// Global mobile dashboard instance
window.mobileDashboard = new MobileDashboard();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileDashboard;
}
