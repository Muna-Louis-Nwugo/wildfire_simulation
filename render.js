// simply get bring the config file into the render
//console.log("Hello World")

let grids;
let jsonGrids;
let selectedGrid;

// Asynchronous function to collect configuration data
const getConfig = async() => {
    const gridData = await fetch("config.json");
    grids = await gridData.json();  // parses the JSON
    console.log(grids);

    selectedGrid = "suburban"

    const fireData = await fetch("update.json");
    let on_fire = await fireData.json();
    console.log(on_fire);

    const damage = await fetch("damage.json");
    let damageCost = await damage.json();
    console.log(damageCost)

    // post something to the HTTP server
    const url = "http://localhost:5000";
    const data = {
    "humidity": 0.3,
    "wind_speed":  12,
    "wind_direction": [12, 3],
    "grid": selectedGrid,
    "fire_start": [3, 8]
    };

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    fetch(url, options)
        .then(response => {
            // Check if the response was successful (status code in 2xx range)
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Parse the JSON response
        })
        .then(responseData => {
            console.log('Success:', responseData); // Handle the successful response
        })
        .catch(error => {
            console.error('Error:', error); // Handle any errors during the fetch or parsing
        });
}

getConfig();
