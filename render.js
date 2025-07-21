// ==================== SIMPLE WILDFIRE SIMULATION ====================

console.log('🔥 Wildfire Simulation Loading...');

// Global state
let grids = {};
let selectedGrid = null;
let selectedCell = null;
let isSimulationRunning = false;
let pollInterval = null;
let currentDamage = 0;

// Make server status interval accessible globally
window.serverStatusInterval = null;

// Cell type to emoji mapping
const CELL_EMOJIS = {
    'forest': '🌲',
    'grass': '🌱', 
    'road': '🛣️',
    'water': '💧',
    'Office': '🏢',
    'Warehouse': '🏭',
    'Concrete House': '🏠',
    'Mansion': '🏰',
    'Apartment Complex': '🏬',
    'Shopping Mall': '🏪',
    'Mall': '🏪',
    'Strip Mall': '🏪',
    'Barn': '🚜',
    'Shack': '🛖',
    'Infrastructure': '🏛️',
    'StripMall': '🏪'
};

// Simulation parameters
let simulationParams = {
    humidity: 30,
    windSpeed: 12,
    windDirectionX: 1,
    windDirectionY: 0
};

// Screen management
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// Initialize the application
async function initializeApp() {
    try {
        await loadGridConfigurations();
        setupEventListeners();
        showScreen('welcome-screen');
        
        // Set initial status to unknown
        const statusElements = document.querySelectorAll('.server-status');
        statusElements.forEach(element => {
            element.classList.add('server-unknown');
            element.textContent = '🟡 Checking...';
        });
        
        // Start checking after a brief delay
        setTimeout(() => {
            startServerStatusChecking();
        }, 500);
        
        console.log('✅ App initialized successfully');
    } catch (error) {
        console.error('❌ Failed to initialize app:', error);
    }
}

// Check server status
async function checkServerStatus() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1000);
        
        // Use OPTIONS request to check if server is alive - won't trigger simulation
        const response = await fetch('http://localhost:5000', {
            method: 'OPTIONS',
            mode: 'cors',
            signal: controller.signal,
            headers: { 
                'Content-Type': 'application/json'
            }
        });
        
        clearTimeout(timeoutId);
        
        // If we get a 200 response to OPTIONS, server is running
        if (response.ok) {
            updateServerStatus(true);
        } else {
            updateServerStatus(false);
        }
        
    } catch (error) {
        // Server is not reachable
        updateServerStatus(false);
    }
}

// Update server status display
function updateServerStatus(isRunning) {
    const statusElements = document.querySelectorAll('.server-status');
    statusElements.forEach(element => {
        element.classList.remove('server-running', 'server-stopped', 'server-unknown');
        
        if (isRunning) {
            element.classList.add('server-running');
            element.textContent = '🟢 Server Running';
        } else {
            element.classList.add('server-stopped');
            element.textContent = '🔴 Server Stopped';
        }
    });
    
    // Enable/disable shutdown buttons based on server status
    const shutdownButtons = document.querySelectorAll('#shutdown-server-btn, button[onclick*="shutdownServer"]');
    shutdownButtons.forEach(button => {
        button.disabled = !isRunning;
    });
}

// Start checking server status
function startServerStatusChecking() {
    // Initial check
    checkServerStatus();
    
    // Store interval globally
    window.serverStatusInterval = setInterval(checkServerStatus, 3000);
}

// Load grid configurations
async function loadGridConfigurations() {
    const response = await fetch('config.json');
    grids = await response.json();
    
    const availableGrids = Object.keys(grids).filter(gridName => gridName !== 'practice');
    populateGridSelection(availableGrids);
}

// Populate grid selection buttons
function populateGridSelection(gridNames) {
    const container = document.getElementById('grid-buttons');
    container.innerHTML = '';
    
    gridNames.forEach(gridName => {
        const button = document.createElement('button');
        button.className = 'grid-button';
        button.textContent = gridName.replace(/_/g, ' ');
        button.type = 'button';
        button.addEventListener('click', () => selectGrid(gridName));
        container.appendChild(button);
    });
}

// Handle grid selection
function selectGrid(gridName) {
    resetSimulation();
    selectedGrid = gridName;
    document.getElementById('grid-title').textContent = gridName.replace(/_/g, ' ');
    document.getElementById('final-grid-name').textContent = gridName.replace(/_/g, ' ');
    displayGrid(grids[gridName]);
    showScreen('simulation-screen');
}

// Display grid
function displayGrid(gridData) {
    const gridDisplay = document.getElementById('grid-display');
    gridDisplay.innerHTML = '';
    gridDisplay.style.gridTemplateColumns = `repeat(${gridData[0].length}, 50px)`;
    
    gridData.forEach((row, rowIndex) => {
        row.forEach((cellData, colIndex) => {
            const cellElement = document.createElement('div');
            cellElement.className = 'grid-cell';
            cellElement.setAttribute('data-row', rowIndex);
            cellElement.setAttribute('data-col', colIndex);
            cellElement.textContent = CELL_EMOJIS[cellData.cell_type] || '❓';
            cellElement.addEventListener('click', (e) => selectFireStartCell(e, rowIndex, colIndex));
            gridDisplay.appendChild(cellElement);
        });
    });
}

// Handle fire start selection
function selectFireStartCell(event, row, col) {
    if (isSimulationRunning) {
        alert('Simulation is already running!');
        return;
    }
    
    // Check if cell is burnable
    const cellData = grids[selectedGrid][row][col];
    const nonBurnableCells = ['road', 'water'];
    
    if (nonBurnableCells.includes(cellData.cell_type)) {
        alert(`Cannot start fire on ${cellData.cell_type}. Please select a burnable cell.`);
        return;
    }
    
    document.querySelectorAll('.grid-cell.selected').forEach(cell => {
        cell.classList.remove('selected');
    });
    
    event.target.classList.add('selected');
    selectedCell = [row, col];
    
    console.log('🔥 Starting fire at:', row, col);
    startSimulation();
}

// Start simulation
async function startSimulation() {
    if (!selectedGrid || !selectedCell || isSimulationRunning) return;
    
    console.log('🚀 Starting simulation...');
    console.log('Selected grid:', selectedGrid);
    console.log('Selected cell:', selectedCell);
    console.log('Simulation params:', simulationParams);
    
    isSimulationRunning = true;
    currentDamage = 0;
    updateDamageDisplay(0);
    
    document.getElementById('loading-overlay').classList.add('active');
    
    // Clear any existing fire
    document.querySelectorAll('.grid-cell.on-fire').forEach(cell => {
        cell.classList.remove('on-fire');
    });
    
    try {
        console.log('📡 Sending POST request...');
        await postSimulationToBackend();
        console.log('✅ POST request successful, starting polling...');
        startPolling();
    } catch (error) {
        console.error('❌ Simulation error:', error);
        alert('Error starting simulation: ' + error.message);
        endSimulation();
    }
}

// Post to backend
async function postSimulationToBackend() {
    const data = {
        humidity: simulationParams.humidity / 100,
        wind_speed: simulationParams.windSpeed,
        wind_direction: [simulationParams.windDirectionX, simulationParams.windDirectionY],
        grid: selectedGrid,
        fire_start: selectedCell
    };
    
    console.log('📤 POST data:', data);
    
    const response = await fetch('http://localhost:5000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    console.log('📥 Response status:', response.status);
    
    if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('📥 Response data:', result);
    return result;
}

// Start polling
function startPolling() {
    console.log('🔄 Starting polling...');
    
    pollInterval = setInterval(async () => {
        if (!isSimulationRunning) {
            clearInterval(pollInterval);
            return;
        }
        
        try {
            const [fireData, damageData] = await Promise.all([
                fetch('update.json?t=' + Date.now()).then(r => r.json()),
                fetch('damage.json?t=' + Date.now()).then(r => r.json())
            ]);
            
            console.log('Fire data:', fireData);
            console.log('Damage data:', damageData);
            
            // Update damage
            if (typeof damageData === 'number' && damageData >= currentDamage) {
                updateDamageDisplay(damageData);
            }
            
            // Handle fire updates
            if (fireData === 'DONE') {
                console.log('🏁 Simulation complete');
                endSimulation();
            } else if (Array.isArray(fireData) && fireData.length > 0) {
                updateFireDisplay(fireData);
                document.getElementById('loading-overlay').classList.remove('active');
            }
            
        } catch (error) {
            console.error('❌ Polling error:', error);
        }
    }, 500);
}

// Update fire display
function updateFireDisplay(onFireCells) {
    document.querySelectorAll('.grid-cell.on-fire').forEach(cell => {
        cell.classList.remove('on-fire');
    });
    
    onFireCells.forEach(([row, col]) => {
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        if (cell) cell.classList.add('on-fire');
    });
}

// Update damage display
function updateDamageDisplay(damage) {
    currentDamage = damage;
    const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(damage);
    
    document.getElementById('damage-amount').textContent = formatted;
}

// End simulation
function endSimulation() {
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
    
    document.getElementById('loading-overlay').classList.remove('active');
    document.getElementById('final-damage-amount').textContent = 
        document.getElementById('damage-amount').textContent;
    
    isSimulationRunning = false;
    showScreen('end-screen');
}

// Reset simulation
function resetSimulation() {
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
    
    selectedGrid = null;
    selectedCell = null;
    currentDamage = 0;
    isSimulationRunning = false;
    
    document.querySelectorAll('.grid-cell.on-fire, .grid-cell.selected').forEach(cell => {
        cell.classList.remove('on-fire', 'selected');
    });
    
    document.getElementById('loading-overlay').classList.remove('active');
    updateDamageDisplay(0);
}

// Shutdown server - MUST BE GLOBAL
window.shutdownServer = async function() {
    try {
        console.log('🛑 Shutting down server...');
        
        // Stop any running simulation first
        if (isSimulationRunning) {
            isSimulationRunning = false;
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
            }
        }
        
        // Send shutdown request with all required fields
        const shutdownData = {
            humidity: 0.5,
            wind_speed: 10,
            wind_direction: [1, 0],
            grid: selectedGrid || "urban_downtown",
            fire_start: [0, 0],
            simulation_end: true  // This is the key field
        };
        
        console.log('Sending shutdown request:', shutdownData);
        
        const response = await fetch('http://localhost:5000', {
            method: 'POST',
            mode: 'cors',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(shutdownData)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('✅ Server response:', result);
            
            if (result.status === 'shutting_down') {
                // Update UI immediately
                updateServerStatus(false);
                
                // Stop checking server status
                if (window.serverStatusInterval) {
                    clearInterval(window.serverStatusInterval);
                    window.serverStatusInterval = null;
                }
                
                alert('Server has been shut down successfully. Close this window and restart the server with "python fire_spread.py" to run more simulations.');
            }
        } else {
            console.error('❌ Failed to shutdown server - bad response');
            alert('Failed to shutdown server. Please try again.');
        }
    } catch (error) {
        console.error('❌ Error shutting down server:', error);
        // Check if it's a network error (server already down)
        if (error.message.includes('Failed to fetch')) {
            updateServerStatus(false);
            alert('Server appears to be already stopped.');
        } else {
            alert('Error communicating with server: ' + error.message);
        }
    }
}

// Set up event listeners
function setupEventListeners() {
    document.getElementById('back-button').addEventListener('click', () => {
        resetSimulation();
        showScreen('welcome-screen');
    });
    
    document.getElementById('restart-button').addEventListener('click', () => {
        resetSimulation();
        showScreen('welcome-screen');
    });
    
    document.getElementById('new-simulation-btn').addEventListener('click', () => {
        // Clear simulation state but keep the grid
        if (pollInterval) {
            clearInterval(pollInterval);
            pollInterval = null;
        }
        
        selectedCell = null;
        currentDamage = 0;
        isSimulationRunning = false;
        
        // Clear visual states
        document.querySelectorAll('.grid-cell.on-fire, .grid-cell.selected').forEach(cell => {
            cell.classList.remove('on-fire', 'selected');
        });
        
        document.getElementById('loading-overlay').classList.remove('active');
        updateDamageDisplay(0);
    });
    
    // Set up shutdown button event listener
    const shutdownBtn = document.getElementById('shutdown-server-btn');
    if (shutdownBtn) {
        shutdownBtn.addEventListener('click', window.shutdownServer);
    }
    
    setupParameterControls();
}

// Set up parameter controls
function setupParameterControls() {
    const controls = [
        { id: 'humidity', prop: 'humidity', suffix: '%' },
        { id: 'wind-speed', prop: 'windSpeed', suffix: ' m/s' },
        { id: 'wind-direction-x', prop: 'windDirectionX', suffix: '' },
        { id: 'wind-direction-y', prop: 'windDirectionY', suffix: '' }
    ];
    
    controls.forEach(({ id, prop, suffix }) => {
        const slider = document.getElementById(id);
        const display = document.getElementById(id + '-value');
        
        slider.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            simulationParams[prop] = value;
            display.textContent = value + suffix;
        });
    });
}

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (window.serverStatusInterval) {
        clearInterval(window.serverStatusInterval);
    }
    if (pollInterval) {
        clearInterval(pollInterval);
    }
});

// Test server connection (for debugging)
window.testServerConnection = async function() {
    try {
        console.log('Testing server connection with OPTIONS...');
        const response = await fetch('http://localhost:5000', {
            method: 'OPTIONS',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
            console.log('✅ Server is responding to OPTIONS');
            return true;
        } else {
            console.log('❌ Server returned error:', response.status);
            return false;
        }
    } catch (error) {
        console.log('❌ Cannot reach server:', error.message);
        return false;
    }
}

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', initializeApp);

console.log('✅ Wildfire Simulation Ready!');