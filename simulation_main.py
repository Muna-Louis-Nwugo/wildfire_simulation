import numpy as np
import matplotlib.pyplot as plt

# Define data types for the simulation

cell_dtypes = np.dtype([
    ('type', np.int8), # 0: empty, 1: forest, 2: building, 3: road
    ('on_fire', np.bool_) # Whether the cell is on fire
    ])


# construct the main simulation grid
grid = np.zeros((20, 20), dtype=cell_dtypes)

print(grid)