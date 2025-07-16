# Curation of practice grids
import cells
import json

# Original practice grid
""" practice = [[cells.Forest((0, 0), 0.2), cells.Forest((0, 1), 0.2), cells.Forest((0, 2), 0.2)],
         [cells.Forest((1, 0), 0.3), cells.Grass((1, 1), 0.2), cells.Grass((1, 2), 0.2)],
         [cells.Road((2, 0)), cells.Road((2, 1)), cells.Road((2, 2))],
         [cells.Water((3, 0)), cells.Water((3, 1)), cells.Water((3, 2))],
        ] """

# Urban Downtown Grid - Dense city core
urban_downtown = [
    [cells.Office((0, 0), 0.08, 2500, 8), cells.Office((0, 1), 0.08, 3000, 12), cells.Road((0, 2)), cells.Office((0, 3), 0.08, 2800, 10), cells.Office((0, 4), 0.08, 3200, 15), cells.Road((0, 5)), cells.Office((0, 6), 0.08, 2700, 9), cells.Office((0, 7), 0.08, 3100, 11), cells.Road((0, 8)), cells.Office((0, 9), 0.08, 2900, 13)],
    [cells.ApartmentComplex((1, 0), 0.12, 1800, 6), cells.Road((1, 1)), cells.Road((1, 2)), cells.Road((1, 3)), cells.Road((1, 4)), cells.Road((1, 5)), cells.Road((1, 6)), cells.Road((1, 7)), cells.Road((1, 8)), cells.ApartmentComplex((1, 9), 0.12, 2000, 8)],
    [cells.Road((2, 0)), cells.Road((2, 1)), cells.Mall((2, 2), 0.1, 8000, 2), cells.Mall((2, 3), 0.1, 8000, 2), cells.Infra((2, 4), 0.06, 1500, 3), cells.Office((2, 5), 0.08, 2600, 7), cells.Office((2, 6), 0.08, 2400, 6), cells.Road((2, 7)), cells.Road((2, 8)), cells.Road((2, 9))],
    [cells.Office((3, 0), 0.08, 2300, 5), cells.ApartmentComplex((3, 1), 0.12, 1700, 7), cells.Road((3, 2)), cells.Road((3, 3)), cells.Road((3, 4)), cells.Road((3, 5)), cells.Road((3, 6)), cells.ApartmentComplex((3, 7), 0.12, 1900, 9), cells.Office((3, 8), 0.08, 2500, 8), cells.Office((3, 9), 0.08, 2700, 10)],
    [cells.Office((4, 0), 0.08, 2800, 12), cells.Office((4, 1), 0.08, 3000, 14), cells.Road((4, 2)), cells.Warehouse((4, 3), 0.15, 4000, 1), cells.Warehouse((4, 4), 0.15, 4500, 1), cells.Office((4, 5), 0.08, 2900, 11), cells.Office((4, 6), 0.08, 2600, 9), cells.Road((4, 7)), cells.Office((4, 8), 0.08, 2400, 7), cells.Office((4, 9), 0.08, 2800, 13)],
    [cells.Road((5, 0)), cells.Road((5, 1)), cells.Road((5, 2)), cells.Road((5, 3)), cells.Road((5, 4)), cells.Road((5, 5)), cells.Road((5, 6)), cells.Road((5, 7)), cells.Road((5, 8)), cells.Road((5, 9))],
    [cells.ApartmentComplex((6, 0), 0.12, 1600, 5), cells.Office((6, 1), 0.08, 2200, 6), cells.Road((6, 2)), cells.Office((6, 3), 0.08, 2700, 8), cells.Office((6, 4), 0.08, 2500, 9), cells.ApartmentComplex((6, 5), 0.12, 1800, 7), cells.Office((6, 6), 0.08, 2300, 5), cells.Road((6, 7)), cells.Office((6, 8), 0.08, 2600, 10), cells.ApartmentComplex((6, 9), 0.12, 1700, 6)],
    [cells.Office((7, 0), 0.08, 2400, 7), cells.Road((7, 1)), cells.Road((7, 2)), cells.Road((7, 3)), cells.Road((7, 4)), cells.Road((7, 5)), cells.Road((7, 6)), cells.Road((7, 7)), cells.Road((7, 8)), cells.Office((7, 9), 0.08, 2500, 8)],
    [cells.Office((8, 0), 0.08, 2900, 11), cells.ApartmentComplex((8, 1), 0.12, 1900, 8), cells.Road((8, 2)), cells.Office((8, 3), 0.08, 2800, 12), cells.Office((8, 4), 0.08, 2600, 9), cells.Office((8, 5), 0.08, 2700, 10), cells.ApartmentComplex((8, 6), 0.12, 1800, 7), cells.Road((8, 7)), cells.Office((8, 8), 0.08, 2400, 6), cells.Office((8, 9), 0.08, 2500, 8)],
    [cells.Office((9, 0), 0.08, 3100, 15), cells.Office((9, 1), 0.08, 2800, 12), cells.Road((9, 2)), cells.Office((9, 3), 0.08, 2900, 13), cells.Office((9, 4), 0.08, 3000, 14), cells.Road((9, 5)), cells.Office((9, 6), 0.08, 2700, 11), cells.Office((9, 7), 0.08, 2600, 10), cells.Road((9, 8)), cells.Office((9, 9), 0.08, 2800, 12)]
]

# Suburban Neighborhood Grid - Mixed residential with some commercial
suburban = [
    [cells.ConcreteHome((0, 0), 0.15, 2200, 2), cells.ConcreteHome((0, 1), 0.15, 2400, 2), cells.Road((0, 2)), cells.ConcreteHome((0, 3), 0.15, 2100, 2), cells.ConcreteHome((0, 4), 0.15, 2300, 2), cells.Road((0, 5)), cells.Mansion((0, 6), 0.12, 4500, 3), cells.Mansion((0, 7), 0.12, 4800, 3), cells.Road((0, 8)), cells.ConcreteHome((0, 9), 0.15, 2000, 2)],
    [cells.ConcreteHome((1, 0), 0.15, 2300, 2), cells.Road((1, 1)), cells.Road((1, 2)), cells.Road((1, 3)), cells.Road((1, 4)), cells.Road((1, 5)), cells.Road((1, 6)), cells.Road((1, 7)), cells.Road((1, 8)), cells.Road((1, 9))],
    [cells.Road((2, 0)), cells.Road((2, 1)), cells.Grass((2, 2), 0.15), cells.Grass((2, 3), 0.15), cells.StripMall((2, 4), 0.15, 1200, 1), cells.StripMall((2, 5), 0.15, 1400, 1), cells.Grass((2, 6), 0.15), cells.Grass((2, 7), 0.15), cells.Road((2, 8)), cells.Road((2, 9))],
    [cells.ConcreteHome((3, 0), 0.15, 2500, 2), cells.ConcreteHome((3, 1), 0.15, 2200, 2), cells.Road((3, 2)), cells.Grass((3, 3), 0.15), cells.Road((3, 4)), cells.Road((3, 5)), cells.Grass((3, 6), 0.15), cells.Road((3, 7)), cells.ConcreteHome((3, 8), 0.15, 2400, 2), cells.ConcreteHome((3, 9), 0.15, 2100, 2)],
    [cells.ConcreteHome((4, 0), 0.15, 2300, 2), cells.Road((4, 1)), cells.Road((4, 2)), cells.Road((4, 3)), cells.Road((4, 4)), cells.Road((4, 5)), cells.Road((4, 6)), cells.Road((4, 7)), cells.Road((4, 8)), cells.ConcreteHome((4, 9), 0.15, 2200, 2)],
    [cells.Road((5, 0)), cells.Road((5, 1)), cells.Forest((5, 2), 0.2), cells.Forest((5, 3), 0.2), cells.Water((5, 4)), cells.Water((5, 5)), cells.Forest((5, 6), 0.2), cells.Forest((5, 7), 0.2), cells.Road((5, 8)), cells.Road((5, 9))],
    [cells.ConcreteHome((6, 0), 0.15, 2400, 2), cells.ConcreteHome((6, 1), 0.15, 2100, 2), cells.Road((6, 2)), cells.Forest((6, 3), 0.2), cells.Water((6, 4)), cells.Water((6, 5)), cells.Forest((6, 6), 0.2), cells.Road((6, 7)), cells.ConcreteHome((6, 8), 0.15, 2300, 2), cells.ConcreteHome((6, 9), 0.15, 2000, 2)],
    [cells.Road((7, 0)), cells.Road((7, 1)), cells.Road((7, 2)), cells.Road((7, 3)), cells.Road((7, 4)), cells.Road((7, 5)), cells.Road((7, 6)), cells.Road((7, 7)), cells.Road((7, 8)), cells.Road((7, 9))],
    [cells.ConcreteHome((8, 0), 0.15, 2200, 2), cells.ConcreteHome((8, 1), 0.15, 2500, 2), cells.Road((8, 2)), cells.ConcreteHome((8, 3), 0.15, 2300, 2), cells.ConcreteHome((8, 4), 0.15, 2100, 2), cells.Road((8, 5)), cells.Mansion((8, 6), 0.12, 4200, 3), cells.Mansion((8, 7), 0.12, 4600, 3), cells.Road((8, 8)), cells.ConcreteHome((8, 9), 0.15, 2400, 2)],
    [cells.ConcreteHome((9, 0), 0.15, 2100, 2), cells.ConcreteHome((9, 1), 0.15, 2300, 2), cells.Road((9, 2)), cells.ConcreteHome((9, 3), 0.15, 2000, 2), cells.ConcreteHome((9, 4), 0.15, 2200, 2), cells.Road((9, 5)), cells.ConcreteHome((9, 6), 0.15, 2400, 2), cells.ConcreteHome((9, 7), 0.15, 2500, 2), cells.Road((9, 8)), cells.ConcreteHome((9, 9), 0.15, 2300, 2)]
]

# Rural Farmland Grid - Farms, forests, and sparse buildings
rural_farmland = [
    [cells.Forest((0, 0), 0.25), cells.Forest((0, 1), 0.25), cells.Forest((0, 2), 0.25), cells.Forest((0, 3), 0.25), cells.Grass((0, 4), 0.2), cells.Grass((0, 5), 0.2), cells.Barn((0, 6), 0.3, 3000, 1), cells.Barn((0, 7), 0.3, 2800, 1), cells.Grass((0, 8), 0.2), cells.Grass((0, 9), 0.2)],
    [cells.Forest((1, 0), 0.25), cells.Forest((1, 1), 0.25), cells.Forest((1, 2), 0.25), cells.Road((1, 3)), cells.Road((1, 4)), cells.Road((1, 5)), cells.Road((1, 6)), cells.Road((1, 7)), cells.Road((1, 8)), cells.Grass((1, 9), 0.2)],
    [cells.Forest((2, 0), 0.25), cells.Forest((2, 1), 0.25), cells.Road((2, 2)), cells.Road((2, 3)), cells.Shack((2, 4), 0.25, 1200, 1), cells.Shack((2, 5), 0.25, 1100, 1), cells.Barn((2, 6), 0.3, 3200, 1), cells.Grass((2, 7), 0.2), cells.Grass((2, 8), 0.2), cells.Grass((2, 9), 0.2)],
    [cells.Water((3, 0)), cells.Water((3, 1)), cells.Water((3, 2)), cells.Road((3, 3)), cells.Grass((3, 4), 0.2), cells.Grass((3, 5), 0.2), cells.Grass((3, 6), 0.2), cells.Grass((3, 7), 0.2), cells.Grass((3, 8), 0.2), cells.ConcreteHome((3, 9), 0.15, 1800, 1)],
    [cells.Water((4, 0)), cells.Water((4, 1)), cells.Water((4, 2)), cells.Road((4, 3)), cells.Grass((4, 4), 0.2), cells.Grass((4, 5), 0.2), cells.Grass((4, 6), 0.2), cells.Grass((4, 7), 0.2), cells.Road((4, 8)), cells.Road((4, 9))],
    [cells.Water((5, 0)), cells.Water((5, 1)), cells.Road((5, 2)), cells.Road((5, 3)), cells.Barn((5, 4), 0.3, 2900, 1), cells.Barn((5, 5), 0.3, 3100, 1), cells.Grass((5, 6), 0.2), cells.Grass((5, 7), 0.2), cells.Grass((5, 8), 0.2), cells.Grass((5, 9), 0.2)],
    [cells.Grass((6, 0), 0.2), cells.Road((6, 1)), cells.Road((6, 2)), cells.ConcreteHome((6, 3), 0.15, 1900, 1), cells.Grass((6, 4), 0.2), cells.Grass((6, 5), 0.2), cells.Grass((6, 6), 0.2), cells.Grass((6, 7), 0.2), cells.Grass((6, 8), 0.2), cells.Forest((6, 9), 0.25)],
    [cells.Grass((7, 0), 0.2), cells.Grass((7, 1), 0.2), cells.Road((7, 2)), cells.Road((7, 3)), cells.Road((7, 4)), cells.Road((7, 5)), cells.Road((7, 6)), cells.Road((7, 7)), cells.Forest((7, 8), 0.25), cells.Forest((7, 9), 0.25)],
    [cells.Grass((8, 0), 0.2), cells.Grass((8, 1), 0.2), cells.Grass((8, 2), 0.2), cells.Shack((8, 3), 0.25, 1000, 1), cells.Barn((8, 4), 0.3, 2700, 1), cells.Barn((8, 5), 0.3, 2500, 1), cells.Grass((8, 6), 0.2), cells.Forest((8, 7), 0.25), cells.Forest((8, 8), 0.25), cells.Forest((8, 9), 0.25)],
    [cells.Grass((9, 0), 0.2), cells.Grass((9, 1), 0.2), cells.Grass((9, 2), 0.2), cells.Grass((9, 3), 0.2), cells.Grass((9, 4), 0.2), cells.Grass((9, 5), 0.2), cells.Forest((9, 6), 0.25), cells.Forest((9, 7), 0.25), cells.Forest((9, 8), 0.25), cells.Forest((9, 9), 0.25)]
]

# Wildland-Urban Interface Grid - Where cities meet wilderness
wildland_urban = [
    [cells.Forest((0, 0), 0.2), cells.Forest((0, 1), 0.2), cells.Forest((0, 2), 0.2), cells.Forest((0, 3), 0.2), cells.Forest((0, 4), 0.2), cells.Forest((0, 5), 0.2), cells.Forest((0, 6), 0.2), cells.Forest((0, 7), 0.2), cells.Forest((0, 8), 0.2), cells.Forest((0, 9), 0.2)],
    [cells.Forest((1, 0), 0.2), cells.Forest((1, 1), 0.2), cells.Forest((1, 2), 0.2), cells.Forest((1, 3), 0.2), cells.Forest((1, 4), 0.2), cells.Forest((1, 5), 0.2), cells.Forest((1, 6), 0.2), cells.Forest((1, 7), 0.2), cells.Forest((1, 8), 0.2), cells.Forest((1, 9), 0.2)],
    [cells.Forest((2, 0), 0.2), cells.Forest((2, 1), 0.2), cells.Forest((2, 2), 0.2), cells.Forest((2, 3), 0.2), cells.Road((2, 4)), cells.Road((2, 5)), cells.Forest((2, 6), 0.2), cells.Forest((2, 7), 0.2), cells.Forest((2, 8), 0.2), cells.Forest((2, 9), 0.2)],
    [cells.Forest((3, 0), 0.2), cells.Forest((3, 1), 0.2), cells.Forest((3, 2), 0.2), cells.Road((3, 3)), cells.Road((3, 4)), cells.Road((3, 5)), cells.Road((3, 6)), cells.ConcreteHome((3, 7), 0.15, 2200, 2), cells.Forest((3, 8), 0.2), cells.Forest((3, 9), 0.2)],
    [cells.Forest((4, 0), 0.2), cells.Forest((4, 1), 0.2), cells.Road((4, 2)), cells.Road((4, 3)), cells.ConcreteHome((4, 4), 0.15, 2100, 2), cells.ConcreteHome((4, 5), 0.15, 2300, 2), cells.Road((4, 6)), cells.Road((4, 7)), cells.Forest((4, 8), 0.2), cells.Forest((4, 9), 0.2)],
    [cells.Forest((5, 0), 0.2), cells.Road((5, 1)), cells.Road((5, 2)), cells.ConcreteHome((5, 3), 0.15, 2000, 2), cells.ConcreteHome((5, 4), 0.15, 2400, 2), cells.ConcreteHome((5, 5), 0.15, 2200, 2), cells.ConcreteHome((5, 6), 0.15, 2100, 2), cells.Road((5, 7)), cells.Road((5, 8)), cells.Forest((5, 9), 0.2)],
    [cells.Road((6, 0)), cells.Road((6, 1)), cells.ConcreteHome((6, 2), 0.15, 2300, 2), cells.ConcreteHome((6, 3), 0.15, 2500, 2), cells.Road((6, 4)), cells.Road((6, 5)), cells.ConcreteHome((6, 6), 0.15, 2000, 2), cells.ConcreteHome((6, 7), 0.15, 2200, 2), cells.Road((6, 8)), cells.Road((6, 9))],
    [cells.Road((7, 0)), cells.Road((7, 1)), cells.Road((7, 2)), cells.Road((7, 3)), cells.Road((7, 4)), cells.Road((7, 5)), cells.Road((7, 6)), cells.Road((7, 7)), cells.Road((7, 8)), cells.Road((7, 9))],
    [cells.ConcreteHome((8, 0), 0.15, 2100, 2), cells.ConcreteHome((8, 1), 0.15, 2400, 2), cells.Road((8, 2)), cells.ApartmentComplex((8, 3), 0.15, 1600, 4), cells.ApartmentComplex((8, 4), 0.15, 1800, 4), cells.Road((8, 5)), cells.ConcreteHome((8, 6), 0.15, 2300, 2), cells.ConcreteHome((8, 7), 0.15, 2000, 2), cells.Road((8, 8)), cells.ConcreteHome((8, 9), 0.15, 2200, 2)],
    [cells.ConcreteHome((9, 0), 0.15, 2200, 2), cells.ConcreteHome((9, 1), 0.15, 2300, 2), cells.Road((9, 2)), cells.Office((9, 3), 0.12, 1800, 3), cells.Office((9, 4), 0.12, 2000, 3), cells.Road((9, 5)), cells.ConcreteHome((9, 6), 0.15, 2400, 2), cells.ConcreteHome((9, 7), 0.15, 2100, 2), cells.Road((9, 8)), cells.ConcreteHome((9, 9), 0.15, 2500, 2)]
]

# Industrial Zone Grid - Warehouses, infrastructure, and industrial buildings
industrial = [
    [cells.Warehouse((0, 0), 0.18, 6000, 1), cells.Warehouse((0, 1), 0.18, 6500, 1), cells.Road((0, 2)), cells.Warehouse((0, 3), 0.18, 5800, 1), cells.Warehouse((0, 4), 0.18, 6200, 1), cells.Road((0, 5)), cells.Warehouse((0, 6), 0.18, 5900, 1), cells.Warehouse((0, 7), 0.18, 6400, 1), cells.Road((0, 8)), cells.Warehouse((0, 9), 0.18, 6100, 1)],
    [cells.Road((1, 0)), cells.Road((1, 1)), cells.Road((1, 2)), cells.Road((1, 3)), cells.Road((1, 4)), cells.Road((1, 5)), cells.Road((1, 6)), cells.Road((1, 7)), cells.Road((1, 8)), cells.Road((1, 9))],
    [cells.Warehouse((2, 0), 0.18, 5700, 1), cells.Warehouse((2, 1), 0.18, 6300, 1), cells.Road((2, 2)), cells.Infra((2, 3), 0.08, 2000, 2), cells.Infra((2, 4), 0.08, 2200, 2), cells.Road((2, 5)), cells.Warehouse((2, 6), 0.18, 6000, 1), cells.Warehouse((2, 7), 0.18, 5800, 1), cells.Road((2, 8)), cells.Warehouse((2, 9), 0.18, 6200, 1)],
    [cells.Road((3, 0)), cells.Road((3, 1)), cells.Road((3, 2)), cells.Road((3, 3)), cells.Road((3, 4)), cells.Road((3, 5)), cells.Road((3, 6)), cells.Road((3, 7)), cells.Road((3, 8)), cells.Road((3, 9))],
    [cells.Warehouse((4, 0), 0.18, 6400, 1), cells.Warehouse((4, 1), 0.18, 5900, 1), cells.Road((4, 2)), cells.Warehouse((4, 3), 0.18, 6100, 1), cells.Warehouse((4, 4), 0.18, 6300, 1), cells.Road((4, 5)), cells.Office((4, 6), 0.12, 1800, 2), cells.Office((4, 7), 0.12, 2000, 2), cells.Road((4, 8)), cells.Warehouse((4, 9), 0.18, 5700, 1)],
    [cells.Road((5, 0)), cells.Road((5, 1)), cells.Road((5, 2)), cells.Road((5, 3)), cells.Road((5, 4)), cells.Road((5, 5)), cells.Road((5, 6)), cells.Road((5, 7)), cells.Road((5, 8)), cells.Road((5, 9))],
    [cells.Warehouse((6, 0), 0.18, 6000, 1), cells.Warehouse((6, 1), 0.18, 6500, 1), cells.Road((6, 2)), cells.Grass((6, 3), 0.15), cells.Grass((6, 4), 0.15), cells.Road((6, 5)), cells.Warehouse((6, 6), 0.18, 5800, 1), cells.Warehouse((6, 7), 0.18, 6200, 1), cells.Road((6, 8)), cells.Office((6, 9), 0.12, 1900, 2)],
    [cells.Road((7, 0)), cells.Road((7, 1)), cells.Road((7, 2)), cells.Road((7, 3)), cells.Road((7, 4)), cells.Road((7, 5)), cells.Road((7, 6)), cells.Road((7, 7)), cells.Road((7, 8)), cells.Road((7, 9))],
    [cells.Warehouse((8, 0), 0.18, 6300, 1), cells.Infra((8, 1), 0.08, 2100, 2), cells.Road((8, 2)), cells.Warehouse((8, 3), 0.18, 5900, 1), cells.Warehouse((8, 4), 0.18, 6400, 1), cells.Road((8, 5)), cells.Warehouse((8, 6), 0.18, 6000, 1), cells.Warehouse((8, 7), 0.18, 5700, 1), cells.Road((8, 8)), cells.Warehouse((8, 9), 0.18, 6100, 1)],
    [cells.Warehouse((9, 0), 0.18, 6200, 1), cells.Warehouse((9, 1), 0.18, 6500, 1), cells.Road((9, 2)), cells.Warehouse((9, 3), 0.18, 5800, 1), cells.Warehouse((9, 4), 0.18, 6300, 1), cells.Road((9, 5)), cells.Warehouse((9, 6), 0.18, 6000, 1), cells.Warehouse((9, 7), 0.18, 5900, 1), cells.Road((9, 8)), cells.Warehouse((9, 9), 0.18, 6400, 1)]
]

# Coastal Community Grid - Mix of residential and water
coastal = [
    [cells.Water((0, 0)), cells.Water((0, 1)), cells.Water((0, 2)), cells.Water((0, 3)), cells.Water((0, 4)), cells.Water((0, 5)), cells.Grass((0, 6), 0.15), cells.ConcreteHome((0, 7), 0.15, 2800, 2), cells.ConcreteHome((0, 8), 0.15, 3000, 2), cells.Mansion((0, 9), 0.12, 5000, 3)],
    [cells.Water((1, 0)), cells.Water((1, 1)), cells.Water((1, 2)), cells.Water((1, 3)), cells.Water((1, 4)), cells.Grass((1, 5), 0.15), cells.Road((1, 6)), cells.Road((1, 7)), cells.Road((1, 8)), cells.Road((1, 9))],
    [cells.Water((2, 0)), cells.Water((2, 1)), cells.Water((2, 2)), cells.Water((2, 3)), cells.Grass((2, 4), 0.15), cells.Grass((2, 5), 0.15), cells.Road((2, 6)), cells.ConcreteHome((2, 7), 0.15, 2600, 2), cells.ConcreteHome((2, 8), 0.15, 2900, 2), cells.Mansion((2, 9), 0.12, 4800, 3)],
    [cells.Water((3, 0)), cells.Water((3, 1)), cells.Water((3, 2)), cells.Grass((3, 3), 0.15), cells.Grass((3, 4), 0.15), cells.Road((3, 5)), cells.Road((3, 6)), cells.Road((3, 7)), cells.Road((3, 8)), cells.Road((3, 9))],
    [cells.Water((4, 0)), cells.Water((4, 1)), cells.Grass((4, 2), 0.15), cells.Grass((4, 3), 0.15), cells.Road((4, 4)), cells.Road((4, 5)), cells.ConcreteHome((4, 6), 0.15, 2700, 2), cells.ConcreteHome((4, 7), 0.15, 2500, 2), cells.ConcreteHome((4, 8), 0.15, 2800, 2), cells.ConcreteHome((4, 9), 0.15, 3100, 2)],
    [cells.Water((5, 0)), cells.Grass((5, 1), 0.15), cells.Grass((5, 2), 0.15), cells.Road((5, 3)), cells.Road((5, 4)), cells.Road((5, 5)), cells.Road((5, 6)), cells.Road((5, 7)), cells.Road((5, 8)), cells.Road((5, 9))],
    [cells.Grass((6, 0), 0.15), cells.Grass((6, 1), 0.15), cells.Road((6, 2)), cells.Road((6, 3)), cells.ConcreteHome((6, 4), 0.15, 2400, 2), cells.ConcreteHome((6, 5), 0.15, 2600, 2), cells.StripMall((6, 6), 0.15, 1500, 1), cells.StripMall((6, 7), 0.15, 1600, 1), cells.Road((6, 8)), cells.ConcreteHome((6, 9), 0.15, 2700, 2)],
    [cells.Grass((7, 0), 0.15), cells.Road((7, 1)), cells.Road((7, 2)), cells.ConcreteHome((7, 3), 0.15, 2500, 2), cells.ConcreteHome((7, 4), 0.15, 2300, 2), cells.Road((7, 5)), cells.Road((7, 6)), cells.Road((7, 7)), cells.Road((7, 8)), cells.Road((7, 9))],
    [cells.Road((8, 0)), cells.Road((8, 1)), cells.ConcreteHome((8, 2), 0.15, 2800, 2), cells.ConcreteHome((8, 3), 0.15, 2600, 2), cells.ConcreteHome((8, 4), 0.15, 2400, 2), cells.Road((8, 5)), cells.Infra((8, 6), 0.08, 1800, 2), cells.ConcreteHome((8, 7), 0.15, 2500, 2), cells.ConcreteHome((8, 8), 0.15, 2700, 2), cells.ConcreteHome((8, 9), 0.15, 2900, 2)],
    [cells.ConcreteHome((9, 0), 0.15, 2700, 2), cells.ConcreteHome((9, 1), 0.15, 2500, 2), cells.ConcreteHome((9, 2), 0.15, 2800, 2), cells.ConcreteHome((9, 3), 0.15, 2600, 2), cells.ConcreteHome((9, 4), 0.15, 2400, 2), cells.Road((9, 5)), cells.ConcreteHome((9, 6), 0.15, 2300, 2), cells.ConcreteHome((9, 7), 0.15, 2500, 2), cells.ConcreteHome((9, 8), 0.15, 2700, 2), cells.ConcreteHome((9, 9), 0.15, 2900, 2)]
]

# list of all grids
grid_dict = {
    "urban_downtown": urban_downtown,
    "suburban": suburban,
    "rural_farmland": rural_farmland,
    "wildland_urban": wildland_urban,
    "industrial": industrial,
    "coastal": coastal
}

# Serializing Data to the Config so it can be used by the render
with open("config.json", "w") as c :
    json.dump(grid_dict, c, default= lambda o: o.__dict__, indent = 4) #default overriden, in order to serialize each individual object 

#make sure the data was serialized properly
with open("config.json", "r") as c :
        grids = json.load(c)
        print("Grid configurations loaded:")
        for grid_name in grids.keys():
            print(f"- {grid_name}")

#CONFIG TO RENDER DATA PIPELINE COMPLETE