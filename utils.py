"""
This file contains every utility module necessessary to transport the information from the backend to the frontend
"""
import  sim_events
import json

#Keeps track of on fire cells
on_fire = []

def newOnFire(cell) -> None :
    coords = cell.get_coordinates()
    #print(coords, [type(c) for c in coords])

    on_fire.append(coords)
    #print(f"{coords}  has been sent to utils") #adds the coordinate to the list of on_fire cells
    #print(f"List of on fire cells {on_fire}")

    with open("update.json", "w") as update :
        json.dump(on_fire, update)

def fireDone(null) -> None :
    with open("update.json", "w") as update :
        json.dump("DONE", update)

    

def set_up_listeners() -> None :
    sim_events.subscribe("fire_update", newOnFire)
    sim_events.subscribe("fire_done", fireDone)



print(sim_events.subscribers)
