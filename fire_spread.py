import numpy as np

#step: grid -> grid
#returns a new grid with the next step of the simulation
def step(grid, height, width):
    new_grid = np.copy(grid)

    for i in range(height): # iterate through each row
        for j in range(width): # iterate through each item in the row
            for k in range(i-1, i+2):
                for l in range(j-1, j+2):
                    #check if the indices are out of bounds
                    if (k > height - 1) or (l > width - 1) or (k < 0) or (l < 0):
                        continue
                    #skips over the current cell
                    if k == i and l == j:
                        continue
                    #check if cells neighboring the current cell are burning
                    elif new_grid[k][l]['on_fire'] == True:
                        grid[i][j]['on_fire'] = True
                        break
                    
    
    return grid