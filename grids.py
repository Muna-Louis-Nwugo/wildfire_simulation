# Curation of practice grids
import cells
import json

practice = [[cells.Forest((0, 0), 0.2), cells.Forest((0, 1), 0.2), cells.Forest((0, 2), 0.2)],
         [cells.Forest((1, 0), 0.3), cells.Grass((1, 1), 0.2), cells.Grass((1, 2), 0.2)],
         [cells.Road((2, 0)), cells.Road((2, 1)), cells.Road((2, 2))],
         [cells.Water((3, 0)), cells.Water((3, 1)), cells.Water((3, 2))],
        ]


# list of all grids
grid_dict = {"practice": practice}


# Serializing Data to the Config so it can be used by the render
with open("config.json", "w") as c :
    json.dump(grid_dict, c, default= lambda o: o.__dict__, indent = 4) #default overriden, in order to serialize each individual object 

#make sure the data was serialized properly
with open("config.json", "r") as c :
        grids = json.load(c)
        print(grids)

#CONFIG TO RENDER DATA PIPELINE COMPLETE