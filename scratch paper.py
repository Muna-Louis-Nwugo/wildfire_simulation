#This is where I practice concepts I learn during the building process

#Cellular automata
# Python code to implement Conway's Game Of Life 
import argparse 
import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib.animation as animation 
  
"""
Basic wildfire CA Logic
1. Each cell is either burning or not burning.
2. Any cell that is burning will burn its neighbors.
3. Program stops when all cells are burning
"""

grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
])
print(grid, '\n')

#run_sim: grid -> grid
#calls step(grid) until all cells are burning
def run_sim(grid):
    while not np.all(grid == 1): # check if all cells are burning
        grid = step(grid)
        print(grid, '\n')
        
    return grid

#step: grid -> grid
#returns a new grid with the next step of the simulation
def step(grid):
    new_grid = np.copy(grid)

    for i in range(len(grid)): # iterate through each row
        for j in range(len(grid[i])): # iterate through each item in the row
            for k in range(i-1, i+2):
                for l in range(j-1, j+2):
                    #check if the indices are out of bounds
                    if (k > len(grid) - 1) or (l > len(grid[i]) - 1) or (k < 0) or (l < 0):
                        continue
                    #print(len(grid[i])-1)
                    #skips over the current cell
                    if k == i and l == j:
                        continue
                    #check if cells neighboring the current cell are burning
                    elif new_grid[k][l] == 1:
                        grid[i][j] = 1
                        break
    
    return grid

run_sim(grid)