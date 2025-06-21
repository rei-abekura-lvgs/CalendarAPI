// Japanese Calendar API Documentation Site JavaScript

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadTodayData();
    initializeQuickAccess();
});

// Initialize the application
function initializeApp() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize Prism.js for code highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }

    // Copy code functionality
    addCopyCodeButtons();
}

// Load today's data for the demo card
async function loadTodayData() {
    const todayDataElement = document.getElementById('today-data');
    
    try {
        const today = new Date();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = today.getDate();
        
        // Get current month data with cache busting
        const cacheBuster = new Date().getTime();
        const response = await fetch(`./api/2025/${month}.json?v=${cacheBuster}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const monthData = await response.json();
        const todayData = monthData.days.find(d => d.day === day);
        
        if (todayData) {
            displayTodayData(todayData);
        } else {
            showTodayDataError('本日のデータが見つかりません');
        }
    } catch (error) {
        console.error('Error loading today data:', error);
        showTodayDataError('データの読み込みに失敗しました');
    }
}

// Display today's data in the demo card
function displayTodayData(data) {
    const todayDataElement = document.getElementById('today-data');
    
    const html = `
        <div class="today-data-item">
            <span class="today-data-label">日付</span>
            <span class="today-data-value">${data.day}日 (${data.weekday})</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">六曜</span>
            <span class="today-data-value">${data.rokuyo}</span>
        </div>
        ${data.is_holiday ? `
        <div class="today-data-item">
            <span class="today-data-label">祝日</span>
            <span class="holiday-badge">${data.holiday_name}</span>
        </div>
        ` : ''}
        <div class="today-data-item">
            <span class="today-data-label">キーワード</span>
            <span class="today-data-value">${data.daily_keyword}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">ラッキーナンバー</span>
            <span class="today-data-value">${data.lucky_number}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">パワーストーン</span>
            <span class="today-data-value">${data.power_stone}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">今日の色</span>
            <span class="today-data-value">${data.color_of_the_day}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">タロットカード</span>
            <span class="today-data-value">${data.tarot_card}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">おすすめお茶</span>
            <span class="today-data-value">${data.recommended_tea}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">瞑想テーマ</span>
            <span class="today-data-value">${data.meditation_theme}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">今日の格言</span>
            <span class="today-data-value">${data.wise_quote}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">推奨音楽</span>
            <span class="today-data-value">${data.recommended_music}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">推奨食材</span>
            <span class="today-data-value">${data.recommended_food}</span>
        </div>
        <div class="today-data-item">
            <span class="today-data-label">風水アドバイス</span>
            <span class="today-data-value">${data.feng_shui_tip}</span>
        </div>
    `;
    
    todayDataElement.innerHTML = html;
}

// Show error message for today's data
function showTodayDataError(message) {
    const todayDataElement = document.getElementById('today-data');
    todayDataElement.innerHTML = `
        <div class="alert alert-warning" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
        </div>
    `;
}

// Test API endpoint functionality
async function testEndpoint(endpoint) {
    const button = event.target;
    const originalText = button.textContent;
    
    // Show loading state
    button.textContent = '読み込み中...';
    button.disabled = true;
    button.classList.add('loading');
    
    try {
        const response = await fetch(`.${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        showEndpointResult(button, data, true);
    } catch (error) {
        console.error('Endpoint test failed:', error);
        showEndpointResult(button, { error: error.message }, false);
    } finally {
        // Reset button state
        setTimeout(() => {
            button.textContent = originalText;
            button.disabled = false;
            button.classList.remove('loading');
        }, 2000);
    }
}

// Show endpoint test result
function showEndpointResult(button, data, success) {
    // Remove any existing result
    const existingResult = button.parentNode.querySelector('.endpoint-result');
    if (existingResult) {
        existingResult.remove();
    }
    
    // Create result element
    const resultElement = document.createElement('div');
    resultElement.className = `endpoint-result ${success ? '' : 'endpoint-error'}`;
    
    if (success) {
        const dataPreview = data.days ? 
            `${data.days.length}日分のデータを取得しました` : 
            `${data.months ? data.months.length : '不明'}ヶ月分のデータを取得しました`;
        
        resultElement.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-check-circle text-success me-2"></i>
                <strong>成功:</strong> ${dataPreview}
            </div>
            <small class="text-muted">詳細はブラウザの開発者ツールをご確認ください</small>
        `;
        console.log('API Response:', data);
    } else {
        resultElement.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-exclamation-circle text-danger me-2"></i>
                <strong>エラー:</strong> ${data.error}
            </div>
        `;
    }
    
    // Insert result after the button's parent
    button.parentNode.appendChild(resultElement);
}

// Add copy code functionality to code blocks
function addCopyCodeButtons() {
    document.querySelectorAll('pre code').forEach((codeBlock) => {
        const pre = codeBlock.parentNode;
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper position-relative';
        
        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-secondary position-absolute';
        copyButton.style.cssText = 'top: 0.5rem; right: 0.5rem; z-index: 1;';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.title = 'コードをコピー';
        
        // Wrap the pre element
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(copyButton);
        wrapper.appendChild(pre);
        
        // Add click event
        copyButton.addEventListener('click', () => {
            copyCodeToClipboard(codeBlock, copyButton);
        });
    });
}

// Copy code to clipboard
async function copyCodeToClipboard(codeBlock, button) {
    const code = codeBlock.textContent;
    const originalContent = button.innerHTML;
    
    try {
        await navigator.clipboard.writeText(code);
        button.innerHTML = '<i class="fas fa-check text-success"></i>';
        button.classList.add('btn-success');
        button.classList.remove('btn-outline-secondary');
        
        setTimeout(() => {
            button.innerHTML = originalContent;
            button.classList.remove('btn-success');
            button.classList.add('btn-outline-secondary');
        }, 2000);
    } catch (err) {
        console.error('Failed to copy code:', err);
        button.innerHTML = '<i class="fas fa-times text-danger"></i>';
        
        setTimeout(() => {
            button.innerHTML = originalContent;
        }, 2000);
    }
}

// Utility function to format JSON
function formatJSON(obj, indent = 2) {
    return JSON.stringify(obj, null, indent);
}

// Utility function to validate date
function isValidDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadTodayData,
        testEndpoint,
        displayTodayData
    };
}

// Quick Access functionality
function initializeQuickAccess() {
    generateMonthLinks(2025); // Default year
    generateYearDataLinks(2025);
    
    // Year button click handlers
    document.querySelectorAll('.year-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const year = parseInt(this.dataset.year);
            
            // Update active state
            document.querySelectorAll('.year-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Update display
            document.getElementById('selected-year').textContent = year;
            generateMonthLinks(year);
            generateYearDataLinks(year);
        });
    });
}

function generateMonthLinks(year) {
    const container = document.getElementById('month-links');
    const months = ['1月', '2月', '3月', '4月', '5月', '6月', 
                   '7月', '8月', '9月', '10月', '11月', '12月'];
    
    container.innerHTML = '';
    
    months.forEach((month, index) => {
        const monthNum = String(index + 1).padStart(2, '0');
        const col = document.createElement('div');
        col.className = 'col-4 col-md-3';
        
        const link = document.createElement('a');
        link.href = `https://rei-abekura-lvgs.github.io/CalendarAPI/api/${year}/${monthNum}.json`;
        link.target = '_blank';
        link.className = 'btn btn-outline-primary btn-sm w-100';
        link.textContent = month;
        
        col.appendChild(link);
        container.appendChild(col);
    });
}

function generateYearDataLinks(year) {
    const container = document.getElementById('year-data-links');
    const formats = [
        { ext: 'json', name: 'JSON', class: 'btn-primary', icon: 'fas fa-download' },
        { ext: 'csv', name: 'CSV', class: 'btn-outline-success', icon: 'fas fa-file-csv' },
        { ext: 'xml', name: 'XML', class: 'btn-outline-warning', icon: 'fas fa-file-code' },
        { ext: 'txt', name: 'TXT', class: 'btn-outline-info', icon: 'fas fa-file-alt' }
    ];
    
    container.innerHTML = '';
    
    formats.forEach(format => {
        const link = document.createElement('a');
        link.href = `https://rei-abekura-lvgs.github.io/CalendarAPI/api/${year}/all.${format.ext}`;
        link.target = '_blank';
        link.className = `btn ${format.class} btn-sm w-100`;
        link.innerHTML = `<i class="${format.icon} me-2"></i>${format.name}形式`;
        
        container.appendChild(link);
    });
}
