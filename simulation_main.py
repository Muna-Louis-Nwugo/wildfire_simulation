import numpy as np
import matplotlib.pyplot as plt
from fire_spread import step

# Define data types for the simulation

cell_dtypes = np.dtype([
    ('type', np.int8), # 0: empty, 1: forest, 2: building, 3: road
    ('on_fire', np.bool_) # Whether the cell is on fire
    ])


# construct the preliminary simulation grid, test whether changing the dtype works
gridWidth, gridHeight = (20, 15)
grid = np.zeros((gridHeight, gridWidth), dtype=cell_dtypes)
grid[1][1] = (1, False)  # Set a cell to Forest
grid[5][5] = (1, True)  # Set a cell to Burning Forest
plt.figure(figsize=(7, 7)) #creates a figure with the specified size


"""
Implementation of basic wildfire CA Logic
1. Each cell is either burning or not burning.
2. Any cell that is burning will burn its neighbors.
3. Program stops when all cells are burning
"""

#show_grid: grid String -> image
#visualizes the grid
def show_grid(g, t):
    plt.clf() # clear the figure
    plt.imshow(g, cmap='plasma') #visualize the grid
    plt.title(t)


#run_sim: grid -> grid
#calls step(grid) until all cells are burning
def run_sim(grid):

    while not np.all(grid['on_fire']): # check if all cells are burning
        show_grid(grid['on_fire'], "Wildfire Sim") # show the grid
        plt.show(block=False) # show the grid without blocking the code
        plt.pause(0.5) # pause for a short time to allow the grid to be displayed
        grid = step(grid, height=gridHeight, width=gridWidth)
    
    show_grid(grid['on_fire'], "Sim complete") # show the final grid
    print("All cells are burning!")
    return grid

run_sim(grid)