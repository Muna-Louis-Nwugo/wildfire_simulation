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

print(g.set_weights(grids.grid1, 0, 5, (-3, -1), (0, 0)))


