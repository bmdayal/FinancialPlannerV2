// Financial Planner Web Application - JavaScript

// Global state
let currentSessionId = null;
let selectedPlans = new Set();

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    loadAvailablePlans();
    setupEventListeners();
});

// ============================================================================
// EVENT LISTENERS
// ============================================================================

function setupEventListeners() {
    // Form submission
    document.getElementById('userInfoForm').addEventListener('submit', handleFormSubmit);
    
    // Chat form
    document.getElementById('chatForm').addEventListener('submit', (e) => e.preventDefault());
}

// ============================================================================
// LOAD AVAILABLE PLANS
// ============================================================================

async function loadAvailablePlans() {
    try {
        const response = await fetch('/api/plans');
        const plans = await response.json();
        
        const plansGrid = document.getElementById('plansGrid');
        plansGrid.innerHTML = '';
        
        plans.forEach(plan => {
            const planCard = document.createElement('div');
            planCard.className = 'plan-card';
            planCard.innerHTML = `
                <input type="checkbox" name="plans" value="${plan.id}" onchange="togglePlan('${plan.id}', this)">
                <div class="plan-icon">${plan.icon}</div>
                <h3>${plan.name}</h3>
                <p>${plan.description}</p>
            `;
            plansGrid.appendChild(planCard);
        });
    } catch (error) {
        console.error('Error loading plans:', error);
        showError('Failed to load available plans');
    }
}

// ============================================================================
// PLAN SELECTION
// ============================================================================

function togglePlan(planId, checkbox) {
    if (checkbox.checked) {
        selectedPlans.add(planId);
    } else {
        selectedPlans.delete(planId);
    }
    
    // Update form visibility
    updateFormVisibility();
    
    // Update card styling
    const card = checkbox.closest('.plan-card');
    if (checkbox.checked) {
        card.classList.add('selected');
    } else {
        card.classList.remove('selected');
    }
}

function updateFormVisibility() {
    // Show/hide form sections based on selected plans
    document.getElementById('retirementSection').style.display = 
        selectedPlans.has('retirement') ? 'block' : 'none';
    document.getElementById('insuranceSection').style.display = 
        selectedPlans.has('insurance') ? 'block' : 'none';
    document.getElementById('estateSection').style.display = 
        selectedPlans.has('estate') ? 'block' : 'none';
    document.getElementById('wealthSection').style.display = 
        selectedPlans.has('wealth') ? 'block' : 'none';
    document.getElementById('educationSection').style.display = 
        selectedPlans.has('education') ? 'block' : 'none';
    document.getElementById('taxSection').style.display = 
        selectedPlans.has('tax') ? 'block' : 'none';
}

// ============================================================================
// FORM HANDLING
// ============================================================================

async function handleFormSubmit(event) {
    event.preventDefault();
    
    if (selectedPlans.size === 0) {
        showError('Please select at least one planning option');
        return;
    }
    
    // Collect user information
    const userInfo = {
        age: parseInt(document.getElementById('age').value),
        annual_income: parseFloat(document.getElementById('annual_income').value),
        savings: parseFloat(document.getElementById('savings').value),
    };
    
    // Add optional fields based on selected plans
    if (selectedPlans.has('retirement')) {
        userInfo.retirement_age = parseInt(document.getElementById('retirement_age').value);
        userInfo.risk_tolerance = document.getElementById('risk_tolerance_retirement').value;
    }
    
    if (selectedPlans.has('insurance')) {
        userInfo.num_dependents = parseInt(document.getElementById('num_dependents').value) || 0;
        userInfo.debts = parseFloat(document.getElementById('debts').value) || 0;
    }
    
    if (selectedPlans.has('estate')) {
        userInfo.num_children = parseInt(document.getElementById('num_children').value) || 0;
        const agesInput = document.getElementById('children_ages').value;
        userInfo.children_ages = agesInput ? agesInput.split(',').map(a => parseInt(a.trim())) : [];
        userInfo.total_assets = userInfo.savings;
    }
    
    if (selectedPlans.has('wealth')) {
        userInfo.risk_tolerance = document.getElementById('risk_tolerance_wealth').value;
        userInfo.total_assets = userInfo.savings;
    }
    
    if (selectedPlans.has('education')) {
        userInfo.num_children = parseInt(document.getElementById('num_children_edu').value) || 0;
        const agesInput = document.getElementById('children_ages_edu').value;
        userInfo.children_ages = agesInput ? agesInput.split(',').map(a => parseInt(a.trim())) : [];
        userInfo.education_savings = parseFloat(document.getElementById('education_savings').value) || 0;
        userInfo.annual_education_contribution = parseFloat(document.getElementById('annual_education_contribution').value) || 0;
    }
    
    if (selectedPlans.has('tax')) {
        userInfo.filing_status = document.getElementById('filing_status').value;
        userInfo.retirement_contributions = parseFloat(document.getElementById('retirement_contributions').value) || 0;
        userInfo.charitable_giving = parseFloat(document.getElementById('charitable_giving').value) || 0;
        userInfo.other_deductions = parseFloat(document.getElementById('other_deductions').value) || 0;
    }
    
    // Show loading spinner with progressive messages
    showLoadingProgress();
    
    try {
        // Start planning
        const response = await fetch('/api/planning/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                selected_plans: Array.from(selectedPlans),
                user_info: userInfo
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate plan');
        }
        
        const result = await response.json();
        currentSessionId = result.session_id;
        
        // Display results
        displayResults(result);
        
        // Switch to results page
        document.getElementById('landingPage').classList.remove('active');
        document.getElementById('resultsPage').classList.add('active');
        
    } catch (error) {
        console.error('Error generating plan:', error);
        showError(error.message || 'Failed to generate financial plan');
    } finally {
        hideLoadingProgress();
    }
}

// ============================================================================
// DISPLAY RESULTS
// ============================================================================

function displayResults(result) {
    // Display executive summary with formatted content
    const executiveSummary = result.plan_summaries['Executive Summary'] || 'No executive summary available';
    document.getElementById('executiveSummary').innerHTML = formatFinancialContent(executiveSummary);
    
    // Display visualizations
    displayVisualizations(result.visualizations);
    
    // Display plan tabs
    displayPlanTabs(result.plan_summaries);
    
    // Initialize chat
    document.getElementById('chatMessages').innerHTML = 
        '<div class="message assistant"><div class="message-content">Hi! I\'m your financial advisor assistant. Ask me any questions about your plan or for clarifications on any recommendations.</div></div>';
}

// ============================================================================
// VISUALIZATIONS
// ============================================================================

function displayVisualizations(visualizations) {
    // Net Worth Chart
    if (visualizations.net_worth) {
        const netWorthDiv = document.getElementById('netWorthChart');
        const data = JSON.parse(visualizations.net_worth);
        Plotly.newPlot(netWorthDiv, data.data, data.layout, { responsive: true });
    }
    
    // Retirement Chart
    if (visualizations.retirement) {
        const retirementDiv = document.getElementById('retirementChart');
        const data = JSON.parse(visualizations.retirement);
        Plotly.newPlot(retirementDiv, data.data, data.layout, { responsive: true });
    } else {
        document.getElementById('retirementChart').style.display = 'none';
    }
    
    // Asset Allocation Chart
    if (visualizations.allocation) {
        const allocationDiv = document.getElementById('allocationChart');
        const data = JSON.parse(visualizations.allocation);
        Plotly.newPlot(allocationDiv, data.data, data.layout, { responsive: true });
    } else {
        document.getElementById('allocationChart').style.display = 'none';
    }
    
    // Budget Chart
    if (visualizations.budget) {
        const budgetDiv = document.getElementById('budgetChart');
        const data = JSON.parse(visualizations.budget);
        Plotly.newPlot(budgetDiv, data.data, data.layout, { responsive: true });
    } else {
        document.getElementById('budgetChart').style.display = 'none';
    }
    
    // Insurance Chart
    if (visualizations.insurance) {
        const insuranceDiv = document.getElementById('insuranceChart');
        const data = JSON.parse(visualizations.insurance);
        Plotly.newPlot(insuranceDiv, data.data, data.layout, { responsive: true });
    } else {
        document.getElementById('insuranceChart').style.display = 'none';
    }
    
    // Education Chart
    if (visualizations.education) {
        const educationDiv = document.getElementById('educationChart');
        const data = JSON.parse(visualizations.education);
        Plotly.newPlot(educationDiv, data.data, data.layout, { responsive: true });
    } else {
        document.getElementById('educationChart').style.display = 'none';
    }

    // Tax Optimization Chart
    if (visualizations.tax_optimization) {
        const taxDiv = document.getElementById('taxOptimizationChart');
        const data = JSON.parse(visualizations.tax_optimization);
        Plotly.newPlot(taxDiv, data.data, data.layout, { responsive: true });
    } else {
        document.getElementById('taxOptimizationChart').style.display = 'none';
    }
}

// ============================================================================
// PLAN TABS
// ============================================================================

function displayPlanTabs(planSummaries) {
    const tabButtons = document.getElementById('planTabs');
    const tabContent = document.getElementById('planContent');
    
    tabButtons.innerHTML = '';
    tabContent.innerHTML = '';
    
    let isFirst = true;
    
    Object.entries(planSummaries).forEach(([planName, summary]) => {
        // Create tab button
        const btn = document.createElement('button');
        btn.className = `tab-btn ${isFirst ? 'active' : ''}`;
        btn.textContent = planName;
        btn.onclick = () => switchTab(planName);
        tabButtons.appendChild(btn);
        
        // Create tab pane
        const pane = document.createElement('div');
        pane.className = `tab-pane ${isFirst ? 'active' : ''}`;
        pane.id = `pane-${planName}`;
        pane.innerHTML = `<div class="plan-header"><h3>${planName}</h3></div><div class="plan-content">${formatFinancialContent(summary)}</div>`;
        tabContent.appendChild(pane);
        
        isFirst = false;
    });
}

function switchTab(planName) {
    // Deactivate all tabs
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
    
    // Activate selected tab
    event.target.classList.add('active');
    document.getElementById(`pane-${planName}`).classList.add('active');
}

// ============================================================================
// CHAT
// ============================================================================

async function sendMessage(event) {
    event.preventDefault();
    
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message || !currentSessionId) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    chatInput.value = '';
    
    // Show loading indicator
    const loadingMessageId = addLoadingMessage();
    
    try {
        // Send message to server
        const response = await fetch(`/api/chat/${currentSessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response');
        }
        
        const result = await response.json();
        
        // Remove loading indicator and add assistant response
        removeLoadingMessage(loadingMessageId);
        addMessageToChat('assistant', result.message);
        
    } catch (error) {
        console.error('Error sending message:', error);
        removeLoadingMessage(loadingMessageId);
        addMessageToChat('assistant', 'Sorry, I encountered an error processing your question. Please try again.');
    }
}

function addMessageToChat(role, content) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Format AI responses with the same formatting as plan content
    if (role === 'assistant') {
        contentDiv.innerHTML = formatFinancialContent(content);
    } else {
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ============================================================================
// UTILITIES
// ============================================================================

function showError(message) {
    alert(`Error: ${message}`);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function downloadPlan(format = 'pdf') {
    if (!currentSessionId) {
        showError('No plan to download');
        return;
    }
    
    // Show loading indicator
    const downloadBtn = document.querySelector('.btn[onclick="downloadPlan()"]');
    const originalText = downloadBtn ? downloadBtn.textContent : '';
    if (downloadBtn) {
        downloadBtn.textContent = 'Generating...';
        downloadBtn.disabled = true;
    }
    
    const downloadUrl = format === 'json' 
        ? `/api/export/${currentSessionId}`
        : `/api/export/${currentSessionId}/${format}`;
    
    if (format === 'json') {
        // Handle JSON download (original functionality)
        fetch(downloadUrl)
            .then(response => response.json())
            .then(data => {
                const element = document.createElement('a');
                element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 2)));
                element.setAttribute('download', `financial_plan_${new Date().toISOString().split('T')[0]}.json`);
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
            })
            .catch(error => {
                console.error('Error downloading plan:', error);
                showError('Failed to download plan');
            })
            .finally(() => {
                if (downloadBtn) {
                    downloadBtn.textContent = originalText;
                    downloadBtn.disabled = false;
                }
            });
    } else {
        // Handle PDF/DOCX download
        fetch(downloadUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Download failed');
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const element = document.createElement('a');
                element.href = url;
                element.download = `financial_plan_${new Date().toISOString().split('T')[0]}.${format}`;
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('Error downloading plan:', error);
                showError('Failed to download plan');
            })
            .finally(() => {
                if (downloadBtn) {
                    downloadBtn.textContent = originalText;
                    downloadBtn.disabled = false;
                }
            });
    }
}

function showDownloadMenu() {
    if (!currentSessionId) {
        showError('No plan to download');
        return;
    }
    
    // Create download menu
    const existingMenu = document.getElementById('downloadMenu');
    if (existingMenu) {
        existingMenu.remove();
    }
    
    const menu = document.createElement('div');
    menu.id = 'downloadMenu';
    menu.className = 'download-menu';
    menu.innerHTML = `
        <div class="download-menu-content">
            <h4>Download Format</h4>
            <button class="download-option" onclick="downloadPlan('pdf'); hideDownloadMenu();">
                📄 PDF Document
                <small>Professional formatted report</small>
            </button>
            <button class="download-option" onclick="downloadPlan('docx'); hideDownloadMenu();">
                📝 Word Document
                <small>Editable DOCX format</small>
            </button>
            <button class="download-option" onclick="downloadPlan('json'); hideDownloadMenu();">
                💾 JSON Data
                <small>Raw data format</small>
            </button>
            <button class="download-cancel" onclick="hideDownloadMenu();">Cancel</button>
        </div>
    `;
    
    document.body.appendChild(menu);
    
    // Close menu when clicking outside
    setTimeout(() => {
        document.addEventListener('click', function closeMenu(e) {
            if (!menu.contains(e.target)) {
                hideDownloadMenu();
                document.removeEventListener('click', closeMenu);
            }
        });
    }, 100);
}

function hideDownloadMenu() {
    const menu = document.getElementById('downloadMenu');
    if (menu) {
        menu.remove();
    }
}

function resetApp() {
    // Reset state
    currentSessionId = null;
    selectedPlans.clear();
    
    // Reset form
    document.getElementById('userInfoForm').reset();
    
    // Reset plan selections
    document.querySelectorAll('input[name="plans"]').forEach(cb => {
        cb.checked = false;
        cb.closest('.plan-card').classList.remove('selected');
    });
    
    // Update form visibility
    updateFormVisibility();
    
    // Switch to landing page
    document.getElementById('resultsPage').classList.remove('active');
    document.getElementById('landingPage').classList.add('active');
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// ============================================================================
// CONTENT FORMATTING
// ============================================================================

function formatFinancialContent(content) {
    if (!content) return '';
    
    // Convert basic markdown-like formatting to HTML
    let formatted = content
        // Headers (#### -> h5, ### -> h4, ## -> h3, # -> h2)
        .replace(/^##### (.+)$/gm, '<h6 class="subsection-header">$1</h6>')
        .replace(/^#### (.+)$/gm, '<h5 class="subsection-header">$1</h5>')
        .replace(/^### (.+)$/gm, '<h4 class="section-header">$1</h4>')
        .replace(/^## (.+)$/gm, '<h3 class="plan-section">$1</h3>')
        .replace(/^# (.+)$/gm, '<h2 class="main-header">$1</h2>')
        
        // Bold text (**text** -> <strong>text</strong>)
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        
        // Lists (- item -> <li>item</li>)
        .replace(/^- (.+)$/gm, '<li class="plan-item">$1</li>')
        
        // Numbered lists (1. item -> <li>item</li>)
        .replace(/^\d+\.\s+(.+)$/gm, '<li class="numbered-item">$1</li>')
        
        // Dollar amounts ($X,XXX.XX -> highlighted span)
        .replace(/\$([0-9,]+(?:\.[0-9]{2})?)/g, '<span class="currency">$$$1</span>')
        
        // Percentages (X% -> highlighted span)  
        .replace(/(\d+(?:\.\d+)?%)/g, '<span class="percentage">$1</span>')
        
        // Years (X years -> highlighted)
        .replace(/(\d+)\s+years?/g, '<span class="timeframe">$1 years</span>')
        
        // Monthly amounts
        .replace(/monthly/gi, '<span class="frequency">monthly</span>')
        .replace(/annually/gi, '<span class="frequency">annually</span>')
        
        // Fix LaTeX escape characters (\( and \)) and other common escapes
        .replace(/\\?\\\(/g, '(')
        .replace(/\\?\\\)/g, ')')
        .replace(/\\\$/g, '$')
        .replace(/\\%/g, '%')
        
        // Convert common math variables to styled spans
        .replace(/\b([A-Z])\s*=/g, '<span class="math-variable">$1</span> =')
        .replace(/\(([A-Z]+)\)/g, '(<span class="math-variable">$1</span>)')
        .replace(/\b([A-Z]{1,3})\s+is\s+the\b/g, '<span class="math-variable">$1</span> is the');
    
    // Wrap consecutive list items in <ul> or <ol>
    formatted = formatted.replace(/((?:<li class="plan-item">.*?<\/li>\s*)+)/gs, '<ul class="plan-list">$1</ul>');
    formatted = formatted.replace(/((?:<li class="numbered-item">.*?<\/li>\s*)+)/gs, '<ol class="numbered-list">$1</ol>');
    
    // Convert line breaks to paragraphs
    const paragraphs = formatted.split(/\n\s*\n/);
    const htmlParagraphs = paragraphs.map(p => {
        p = p.trim();
        if (!p) return '';
        if (p.startsWith('<h') || p.startsWith('<ul') || p.startsWith('<div')) {
            return p;
        }
        return `<p class="plan-paragraph">${p}</p>`;
    }).filter(p => p);
    
    return htmlParagraphs.join('\n');
}

// ============================================================================
// LOADING INDICATORS
// ============================================================================

function addLoadingMessage() {
    const chatMessages = document.getElementById('chatMessages');
    const loadingId = 'loading-' + Date.now();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = loadingId;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content loading-message';
    contentDiv.innerHTML = `
        <div class="loading-animation">
            <div class="loading-text">AI is thinking</div>
            <div class="loading-dots">
                <span class="dot dot1">●</span>
                <span class="dot dot2">●</span>
                <span class="dot dot3">●</span>
            </div>
        </div>
    `;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return loadingId;
}

function removeLoadingMessage(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

let progressInterval;
let progressStep = 0;

function showLoadingProgress() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const loadingText = loadingSpinner.querySelector('p');
    const subText = loadingSpinner.querySelector('.spinner-subtext');
    
    loadingSpinner.style.display = 'flex';
    
    const progressMessages = [
        {
            main: "Analyzing your financial information...",
            sub: "Our AI is reviewing your current situation"
        },
        {
            main: "Consulting specialized planning agents...",
            sub: "Retirement, insurance, and wealth management experts at work"
        },
        {
            main: "Calculating personalized recommendations...",
            sub: "Running financial models and projections"
        },
        {
            main: "Generating interactive visualizations...",
            sub: "Creating charts and graphs for your plan"
        },
        {
            main: "Finalizing your comprehensive plan...",
            sub: "Almost ready! Putting the finishing touches"
        }
    ];
    
    progressStep = 0;
    
    // Update loading message every 2 seconds
    progressInterval = setInterval(() => {
        if (progressStep < progressMessages.length) {
            loadingText.textContent = progressMessages[progressStep].main;
            subText.textContent = progressMessages[progressStep].sub;
            progressStep++;
        } else {
            // Cycle through last few messages
            const cycleIndex = (progressStep - progressMessages.length) % 2;
            const cycleMessages = progressMessages.slice(-2);
            loadingText.textContent = cycleMessages[cycleIndex].main;
            subText.textContent = cycleMessages[cycleIndex].sub;
            progressStep++;
        }
    }, 2000);
}

function hideLoadingProgress() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    loadingSpinner.style.display = 'none';
    
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    
    // Reset to original message
    const loadingText = loadingSpinner.querySelector('p');
    const subText = loadingSpinner.querySelector('.spinner-subtext');
    loadingText.textContent = "Generating your personalized financial plan...";
    subText.textContent = "This may take a moment as our AI agents analyze your information";
}
