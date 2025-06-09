# 🔥 Wildfire Simulation
##### A 2-D spatial simulation engine demonstrating how wildfires spread across terrain and damage infrastructure using custom graph algorithms and probabilistic modelling.
---
## Start and Run Simulation
``` bash
git clone https://github.com/Muna-Louis-Nwugo/wildfire_simulation.git
cd wildfire_simulation/fire_spread
python
>>> from fire_spread import spread
>>> from grids import grid1
>>> # Usage: spread(grid, humidity: float, wind_speed: float, wind_direction: tuple, fire_start: tuple)
>>> spread(grid1, humidity=30.0, wind_speed=15.0, wind_direction=(2, 9), fire_start=(0, 0))
>>> # Note: grid1 is a 5x5 grid
>>> # More grid options and simpler entry point coming with completed render
```

---
## Overview
This Wildfire Simulation aims to realistically model the spread of a fire across diverse terrains from city to rural, eventually aiming to simulate the cost of damage to infrastructure that wildfires cause under specific conditions. 

It works by:
- using a grid layered on top of 2 separate custom BFS traversals:
  1. The first to estimate a fire's spread probability between each cell
  2. The second to stochastically propagate the fire throughout the grid (replacing a Cellular Automaton approach for a more elegant solution)
- Using an event-driven approach to dynamically update the render as new cells catch fire and burn out.

  ## ADD EQUATIONS

---
## System Architecture

```
Location Data ---> Config <--- Cell Objects
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

### Config, Location Data and Cell Objects
- Information used to load maps and weather parameters
  - Location Data loaded off of a weather API (not decided yet)
  - Cell objects include all information about a cell (including equations needed to compute probability)
  -   Crucially, cells are not aware of their own fire state

### Render [Starting point]
- Visual representation of the grid
- Allows users to select a configuration and sends that configuration to fire spread
- Observes SimEvents to be notified when the fire state is updated

### Fire Spread
- Sends user preferences to Graph Builder, receives a graph
- Performs a probabilistic spread of the fire on the graph, sending updates to sim events every time a new fire is lit

### Graph Builder [The utility module]
- Takes a grid and returns a graph that fire spread can operate on

### SimEvents [The Event Broker]
- Ferries fire state data from Fire Spread to Render
