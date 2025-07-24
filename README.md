# 🔥 Wildfire Simulation
##### A 2D spatial simulation engine that models wildfire spread across terrain and estimates infrastructure damage using custom graph algorithms and probabilistic modeling.

Inspired by the 2025 Los Angeles wildfires, this project was born from a desire to help people and governments better prepare for potential catastrophes. Originally planned as a tool to assess wildfire risk by region, this prototype now aims to provide citizens, local governments, and insurance agencies with insight into the potential damage a wildfire could cause to real estate in various U.S. regions.

###### Disclaimer: This project emphasizes custom backend architecture and system design, including a novel event-driven communication layer between Python simulation engine and web interface. Frontend components were rapidly prototyped using modern development tools to accelerate time-to-deployment while maintaining focus on core simulation algorithms and infrastructure damage modeling.

---
## Start and Run Simulation
Clone the repo
```
git clone https://github.com/Muna-Louis-Nwugo/wildfire_simulation.git
```
Terminal 1 - Start Backend:
```
cd wildfire_simulation
python fire_spread.py
```

Terminal 2 - Start Front-end:
```
cd wildfire_simulation
python -m http.server 6600
```
Open Browser (Note, use chrome for full functionality):
```
http://localhost:6600/render.html
```

### How to Use
1. Select a terrain type from the welcome screen (Urban, Suburban, Rural, etc.)
2. Adjust simulation parameters (humidity, wind speed, wind direction)
3. Click any cell on the grid to start the fire
4. Watch the fire spread in real-time with damage cost tracking
5. View final damage cost estimation when the simulation completes

---
## Overview
This Wildfire Simulation aims to realistically model the spread of a fire across diverse terrains from city to rural with the main purpose of simulating the cost of damage to infrastructure that wildfires cause under specific conditions. 

It works by:
- using a grid layered on top of 2 separate custom BFS traversals:
  1. The first to estimate a fire's spread probability between each cell
  2. The second to stochastically propagate the fire throughout the grid (replacing a Cellular Automaton approach for a less clunky, more elegant solution)
- Using an event-driven approach to dynamically update the render as new cells catch fire and burn out.

A fire's spread probability is estimated using the following Compound formula:
### Spread Probability = (Base Probability) * (Flammability Factor) * (Wind Factor)
Where:
- **Base Probability** is set to 0.5 (50% chance of spread if nothing else was considered)
- **Flammability Factor** = (_FFuel_) * (1 - (_MFuel_ / _MExt_)) * (1 - _Humidity_); where:
  - _FFuel_: Flammability of fuel when completely dry
  - _MFuel_: Fraction of moist Weight in fuel
  - _MExt_: threshold of moist weight in fuel before it can no longer burn
  - _Humidity_ : Ambient humidity of environment
- **Wind Factor** = e^((_wind coefficient_) * (_Wind Speed_) * cos(_Spread Direction_)); where:
  - _wind coefficient_: Determines how strongly wind influences spread (set to 0.35 for a more natural variation in spread)
  - _Wind Speed_: Speed of the wind in meters per second
  - _Spread Direction_: Angle between wind direction and direction the program is considering spreading into

The damage cost equation was only applied to buildings for simplicity's sake, but is as follows
### Total Cost = (Cost per Square Foot) * (Floor Area) * (Num Floors)

---
## System Architecture

```
    --------> Render <---------
    |           |              |
    |           |              |
  Utils         |              |
    ^           |              |
    |           |              |---- Grids <--Cell Objects
    |           |              |
Sim_Events      |              |
    ^           |              |
    |           V              |
    ------- Fire_Spread <------
              |    ^
              V    |
            Graph_Builder
```

### Grids and Cell Objects [The Data Module]
- Information used to load maps and weather parameters
  - Grids stores every grid configuration supported by the system 
  - Cell objects contain all cell-specific data (including equations needed to compute probability), this does not include fire-state, this was necessary for proper separation of concers

### Render [The Starter Module]
- Visual representation of the grid
- Allows users to select a configuration and sends that configuration to Fire Spread through an HTTP Post request
- Polls updates from specified JSON files to glean data from the backend and display it to the user

### Fire Spread [The Brains]
- Starts and maintains HTTP server to receive user input information from Render
- Sends user preferences to Graph Builder, receives a graph
- Performs a probabilistic spread of the fire on the graph, sending updates to sim events every time a new fire is lit
- Posts information about fire state to Sim_Events

### Graph Builder [The Helper]
- Takes a grid and returns a graph that fire spread can operate on

### Sim_Events [The Event Broker]
- Ferries fire state data from Fire Spread to the Utils Module

### Utils [The Utility Module]
- updates JSON files with appropriate fire spread data to be read by the render



### Communication Layer
Since this project required communication between web-based JavaScript and machine-executable Python, A custom communication layer was needed to circumvent the browser's sanboxing and JavaScript's incompatabilities with Python. My solution was to use an HTTP server for Render -> Fire Spread communication, but then to have Render read data from JSON files to track fire updates. This is mainly because I had already designed my system around using JSON files to communicate before I realized that the browser's sandboxing prevented browser-based programs from writing to files on the machine. After setting up the HTTP server, I decided that in order to maintain separation of concerns (and also because I had already written this part of the system) I was going to have the front-end simply read from JSON files that the Utils module writes to.

---
## Technologies Used
1. Vanilla Python (all methods developed solo)
2. JavaScript (Rendering)
3. Modular, Event-Driven Architecture
4. Object-Oriented Design
5. Observer Pattern
6. Stochastic Modelling
7. Two-Stage Algorithm Design (Graph-building + simulation)
8. Graph-Based Spatial Algorithms
9. Breadth First Search (Customised for this use case)
10. Hypertext Transfer Protocol
11. JSON Handling
12. Full Stack Development

### Planned
1. API integration (Real-time weather data)

---
## Project Status
### Complete
- Full Fire Spread Simulation Engine
- Elementary Cell Object Configurations (e.g. forest, grass, water, road)
- Rendering
- Damage Cost Estimation Engine

### In Progress
- API Integration
