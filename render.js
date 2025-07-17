// ==================== WILDFIRE SIMULATION ====================

console.log('🔥 Wildfire Simulation Loading...');

// Global state
let grids = {};
let selectedGrid = null;
let selectedCell = null;
let isSimulationRunning = false;
let pollInterval = null;
let currentDamage = 0;

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
        console.log('✅ App initialized successfully');
    } catch (error) {
        console.error('❌ Failed to initialize app:', error);
    }
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
    if (isSimulationRunning) return;
    
    document.querySelectorAll('.grid-cell.selected').forEach(cell => {
        cell.classList.remove('selected');
    });
    
    event.target.classList.add('selected');
    selectedCell = [row, col];
    startSimulation();
}

// Start simulation
async function startSimulation() {
    if (!selectedGrid || !selectedCell || isSimulationRunning) return;
    
    console.log('🚀 Starting simulation...');
    isSimulationRunning = true;
    currentDamage = 0;
    updateDamageDisplay(0);
    
    document.getElementById('loading-overlay').classList.add('active');
    document.querySelectorAll('.grid-cell.on-fire').forEach(cell => {
        cell.classList.remove('on-fire');
    });
    
    try {
        await postSimulationToBackend();
        await new Promise(resolve => setTimeout(resolve, 1000));
        startPolling();
    } catch (error) {
        console.error('❌ Simulation error:', error);
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
    
    const response = await fetch('http://localhost:5000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
    }
    
    return response.json();
}

// Start polling
function startPolling() {
    let hasSeenFire = false;
    
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
            
            // Update damage
            if (typeof damageData === 'number' && damageData >= currentDamage) {
                updateDamageDisplay(damageData);
            }
            
            // Handle fire updates
            if (fireData === 'DONE' && hasSeenFire) {
                console.log('🏁 Simulation complete');
                endSimulation();
            } else if (Array.isArray(fireData) && fireData.length > 0) {
                hasSeenFire = true;
                updateFireDisplay(fireData);
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

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', initializeApp);

console.log('✅ Wildfire Simulation Ready!');