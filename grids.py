# Curation of practice grids
import cells

grid1 = [[cells.Forest((0, 0), 0.2), cells.Forest((0, 1), 0.2), cells.Forest((0, 2), 0.2)],
         [cells.Forest((1, 0), 0.3), cells.Grass((1, 1), 0.2), cells.Grass((1, 2), 0.2)],
         [cells.Road((2, 0)), cells.Road((2, 1)), cells.Road((2, 2))],
         [cells.Water((3, 0)), cells.Water((3, 1)), cells.Water((3, 2))],
        ]