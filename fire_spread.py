from graph_builder import set_weights
from sim_events import post
import random
import grids

"""
TODO: DESCRIPTION
"""

def spread(grid: list, humidity: float, wind_speed: float, wind_direction: tuple, fire_start: tuple) :
    fire_graph = set_weights(grid, humidity, wind_speed, wind_direction, fire_start)

    #keep track of on_fire cells
    on_fire = set()
    
    #keep track of queue
    queue = set()

    #add the first item to both on_fire and queue
    on_fire.add(fire_start)
    queue.add(fire_start)

    # loops through queue
    while len(queue) > 0 :
        current_cell = queue.pop()


        for neighbour, weight in fire_graph[current_cell].items() :
            if neighbour not in on_fire:
                if random.random() <= weight:
                    print(f"{neighbour} caught fire")
                    on_fire.add(neighbour)
                    queue.add(neighbour)
                    post("Fire update", neighbour)
    
    post("Fire done", None)

spread(grids.grid1, 0.5, 10, (2, 9), (1, 0))
