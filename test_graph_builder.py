import pytest
import graph_builder as g
import grids

def test_get_neighbors() -> None:
    assert g.get_neighbors((0, 0), grids.grid1) == set([(0, 1), (1, 0), (1, 1)])
    assert g.get_neighbors((0, 1), grids.grid1) == set([(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)])
    assert g.get_neighbors((2, 2), grids.grid1) == set([(1, 1), (1, 2), (2, 1), (3, 1), (3, 2)])
    assert g.get_neighbors((2, 1), grids.grid1) == set([(2, 0), (2, 2), (1, 0), (1, 1), (1, 2), (3, 0), (3, 1), (3, 2)])


def test_make_adj_list() -> None:
    adj = g.make_adj_list(grids.grid1)

    assert adj[(0, 0)] == {(0, 1), (1, 0), (1, 1)}
    assert adj[(0, 1)] == {(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)}
    assert adj[(1, 2)] == {(0, 1), (0, 2), (1, 1), (2, 1), (2, 2)}
    assert adj[(2, 1)] == {(1, 0), (1, 1), (1, 2), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2)}
    assert adj[(3, 0)] == {(2, 0), (2, 1), (3, 1)}

def test_set_weights_valid_range() -> None:
    weighted_graph = g.set_weights(grids.grid1, humidity=0.3, wind_speed=5.0, wind_direction=(1, 0), cell=(0, 0))

    # Confirm output format and values
    for node, neighbors in weighted_graph.items():
        for neighbor, weight in neighbors.items():

            # Grass/Forest cells should return weight > 0
            if node[0] <= 1 and neighbor[0] <= 1:  # top half of grid = burnable
                assert 0.0 <= weight <= 1.0
            # Road/Water cells should return 0
            elif neighbor[0] >= 2:
                assert weight == 0.0

def test_set_weights_water_and_road() -> None:
    weighted_graph = g.set_weights(grids.grid1, humidity=0.1, wind_speed=10.0, wind_direction=(0, 1), cell=(0, 0))

    # Check that water and road cells return 0 probability
    for node, neighbors in weighted_graph.items():
        for neighbor, weight in neighbors.items():
            i, j = neighbor
            if grids.grid1[i][j].cell_type in ['road', 'water']:
                assert weight == 0.0