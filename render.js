// simply get bring the config file into the render
//console.log("Hello World")

/* let grids;

fetch("config.json")
    .then(response => response.json())
    .then(value => {
        grids = value;
        console.log(grids);
    })
    .catch(error => console.error("Something went wrong"));

console.log(grids)
// CONFIG TO RENDER DATA PIPELINE COMPLETE

//const fs = require("fs"); // imports fs (file system) module
let jsonGrids = JSON.stringify(grids);
console.log(jsonGrids) */


let grids;
let jsonGrids;
let selectedGrid;

// Asynchronous function to collect configuration data
const getConfig = async() => {
    const gridData = await fetch("config.json");
    grids = await gridData.json();  // parses the JSON
    console.log(grids);

    selectedGrid = "wildland_urban"




    const fireData = await fetch("update.json");
    let on_fire = await fireData.json();
    console.log(on_fire);
    jsonOnFire = JSON.stringify(on_fire);
    console.log(jsonOnFire)



    // post something to the HTTP server
    const url = "http://localhost:5000";
    const data = {
    "humidity": 0.3,
    "wind_speed":  12,
    "wind_direction": [12, 3],
    "grid": selectedGrid
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

/* grids = getConfig()
    .then(grids => {
        jsonGrids = JSON.stringify(grids);
    }); */
//console.log(grids);
//console.log(jsonGrids);

getConfig();