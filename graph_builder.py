# All things related to constructing the graph for the simulation
# e.g. calulating weight of edges, angle between nodes, etc.
# Utility module, does't affect overall state of simulation

# returns a set of valid neighbours for every cell in a grid
def get_neighbors(cell: tuple, grid: list) -> set:
    neighbors = set()

    # Get the coordinates of the cell
    x, y = cell

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            # Check if the neighbor is within the grid bounds
            if 0 <= x + i < len(grid) and 0 <= y + j < len(grid[0]):
                neighbors.add((x + i, y + j))
    
    return neighbors

#sets up primary adjacency list
def make_adj_list(grid: list) -> dict:
    adj_list = {}

    for i in grid:
        for j in i:
            adj_list[(j.get_coordinates())] = get_neighbors(j.get_coordinates(), grid)
    
    return adj_list



#sets the weights of graph edges
def set_weights(grid: list, humidity: float, wind_speed: float, wind_direction: tuple, cell: tuple) -> dict:
    x, y = cell
    graph = make_adj_list(grid)

    #keeps track of visited cells
    visited = set() 
    #keeps track of which cells are to be visited and which aren't
    to_be_visited = set() 
    to_be_visited.add((x, y))

    while len(to_be_visited) > 0:
        i, j = to_be_visited.pop()
        # keeps track of neighbour weight
        neighbour_weight = {} 

        while len(graph[(i, j)]) > 0 :
            k, l = graph[(i, j)].pop()

            #compute neighbour weight
            neighbour_weight[(k, l)] = grid[k][l].prob_spread(humidity, wind_speed, wind_direction, ((l-j), (k-i)))

            #If cell hasn't been visited, add it to queue
            if (k, l) not in visited :
                to_be_visited.add((k, l)) 
        
        #update graph and add currrent cell to visited set
        graph[(i, j)] = neighbour_weight
        visited.add((i, j))
    
    return graph