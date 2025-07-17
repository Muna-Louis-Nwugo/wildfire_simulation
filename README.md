# 🔥 Wildfire Simulation
##### A 2-D spatial simulation engine demonstrating how wildfires spread across terrain and assess damage to infrastructure using custom graph algorithms and probabilistic modelling.

Inspired by the 2025 Los Angeles Wildfires, this project was born out of a desire to help people and governments better prepare for catastrophes that may occur in their areas. Originally planned to be a tool to help people see the likelihood of a wildfire occurring in their area, this crude tool intends to give citizens, governments and insurance agencies an idea of how much damage a wildfire could cause if started in some regions of the United States.

---
## Start and Run Simulation
```
git clone https://github.com/Muna-Louis-Nwugo/wildfire_simulation.git
cd wildfire_simulation
```
Terminal 1 - Start Backend:
```
python fire_spread.py
```

Terminal 2 - Start Frontend:
```
python -m http.server 8000
```
Open Browser:
```
http://localhost:8000/render.html
```

### How to Use
Select a terrain type from the welcome screen (Urban, Suburban, Rural, etc.)
Adjust simulation parameters (humidity, wind speed, wind direction)
Click any cell on the grid to start the fire
Watch the fire spread in real-time with damage cost tracking
View final results when simulation completes

---
## Overview
This Wildfire Simulation aims to realistically model the spread of a fire across diverse terrains from city to rural, eventually aiming to simulate the cost of damage to infrastructure that wildfires cause under specific conditions. 

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

---
## System Architecture

```
Location Data ---> Config <--- Grid <--- Cell Objects
                      |
                      | [Possible Selections]
                      |
                      V      [Fire State]
                    Render <-------------- SimEvents
                      |                        ^
                      | [User Preferences]     |
                      |                        | [Fire State]
                      V                        |
                  Fire Spread ------------------
                   ^     |
      [Graph Info] |     | [User Preferences]
                   |     |
                   |     V
                Graph Builder
```

### Config, Location Data, Grid and Cell Objects [The Helpers]
- Information used to load maps and weather parameters
  - Location Data loaded off of a weather API (not decided yet)
  - Grid stores every grid configuration supported by the system (plan on letting the user create custom grid configurations)
  - Cell objects contain all cell-specific data (including equations needed to compute probability)
  -   Crucially, cells are not aware of their own fire state

### Render [Starting Point]
- Visual representation of the grid
- Allows users to select a configuration and sends that configuration to Fire Spread
- Observes SimEvents to be notified when the fire state is updated

### Fire Spread [The Brains]
- Sends user preferences to Graph Builder, receives a graph
- Performs a probabilistic spread of the fire on the graph, sending updates to sim events every time a new fire is lit

### Graph Builder [The Utility Module]
- Takes a grid and returns a graph that fire spread can operate on

### SimEvents [The Event Broker]
- Ferries fire state data from Fire Spread to Render

---
## Technologies Used
1. Vanilla Python (all methods developed solo)
2. Modular, Event-Driven Architecture
3. Object-Oriented Design
4. Observer Pattern
5. Stochastic Modelling
6. Two-Stage Algorithm Design (Graph-building + simulation)
7. Graph-Based Spatial Algorithms
8. Breadth First Search (Customised for this use case)

### Planned
1. API integration (Real-time weather data)
2. JavaScript (Rendering)

---
## Project Status
### Complete
- Full Fire Spread Simulation Engine
- Elementary Cell Object Configurations (e.g. forest, grass, water, road)

### In Progress
- Rendering
- API Integration
- Advanced Cell Object Configurations (e.g. high-rise, home, shack)
  - require more sophisticated probability equations

### Planned
- Damage Cost Estimation Engine
