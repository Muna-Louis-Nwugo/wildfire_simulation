"""
This file contains every utility module necessessary to transport the information from the backend to the frontend
"""
import  sim_events
import json

#Keeps track of on fire cells
on_fire = []
cost_damage = 0

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

def updateCost(cell) -> int :
    global cost_damage
    cost_damage += (cell.cost())

    with open("damage.json", "w") as update:
        json.dump(cost_damage, update)

    #print(cost_damage)
    return cost_damage
    
def resetJSON() -> None :
    global on_fire
    global cost_damage
    on_fire = []
    cost_damage = 0

    with open("update.json", "w") as update:
        json.dump(on_fire, update)
    
    with open("damage.json", "w") as update:
        json.dump(cost_damage, update)

def set_up_listeners() -> None :
    resetJSON()
    sim_events.subscribe("fire_update", newOnFire)
    sim_events.subscribe("fire_update", updateCost)
    sim_events.subscribe("fire_done", fireDone)



print(sim_events.subscribers)
