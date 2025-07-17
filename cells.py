#Insert all cell type objects here
from abc import ABC, abstractmethod
import math
import random

# cell union
class Cell(ABC):
    def __init__(self, cell_type: str, 
                 coordinates: tuple, 
                 base_flammability: float, 
                 fuel_moisture: float, 
                 moisture_ext: float) -> None:
        self.cell_type = cell_type
        self.coordinates = coordinates
        self.base_flammability = base_flammability
        self.fuel_moisture = fuel_moisture
        self.moisture_ext = moisture_ext
    

    def get_flammability(self, ambient_humidity: float) -> float:
        return self.base_flammability * (1 - (self.fuel_moisture/self.moisture_ext)) * (1 - ambient_humidity)
        # calculates the flammability of any given cell
    
    

    def wind_effect(self, wind_speed: float, wind_direction: tuple, fire_spread_direciton: tuple) -> float:
        # calculates the effect of wind on the fire spread
        # fire_spraed_direciton is a tuple of the form (x, y)
            #supposed to represent the direction the program is considering the fire to spread
        # wind_direction is a tuple of the form (x, y)
            #supposed to represent the direction the wind is blowing
        # wind_speed is a float value
        # returns a float value
        angle_wind = math.atan2(wind_direction[1], wind_direction[0])
        angle_spread = math.atan2(fire_spread_direciton[1], fire_spread_direciton[0])
        return math.exp(0.35 * wind_speed * math.cos(angle_wind - angle_spread))
    

    def prob_spread(self, ambient_humidity: float, wind_speed: float, wind_direction: tuple, fire_spread_direction: tuple) -> float :
        # calculates the probability of fire spreading to this cell
        # returns a float value
        base_prob = 0.8
        return base_prob * self.get_flammability(ambient_humidity) * self.wind_effect(wind_speed, wind_direction, fire_spread_direction)
    
    #determines the cost of this cell
    def cost(self) -> float:
        return 0
    

    def get_coordinates(self):
        return self.coordinates
    
    def __str__(self) -> str:
        return f"Cell(type={self.cell_type}, coordinates={self.coordinates}, base_flammability={self.base_flammability}, fuel_moisture={self.fuel_moisture}, moisture_ext={self.moisture_ext})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    """ def burn_time(self, ambient_humidity: float, wind_speed: float, wind_direction: tuple, fire_spread_direction: tuple, base_time: float = 0.8) -> float:
        flammability = self.get_flammability(ambient_humidity)
        wind_factor = self.wind_effect(wind_speed, wind_direction, fire_spread_direction)
        moisture_factor = 1 + (self.fuel_moisture / self.moisture_ext)  # More moisture = slower burn

        time = base_time * moisture_factor / (flammability * wind_factor)
        return max(time, 0.5)  # don’t allow zero or negative burn time """



"""
The following are environmental cells (environmental in this case meaning cells that are not buildings). They will not be included in Damage Cost
Estimation, but rather as a sort of catalyst for the spread of the fire, moving the fire across the terrain until they reach the buildings whose 
cost will be estimated
"""

# forest cell
class Forest(Cell):
    def __init__(self, coordinates: tuple, fuel_moisture: float) -> None:
        super().__init__("forest", coordinates, 0.8, fuel_moisture, 0.4)
 
#grass cell
class Grass(Cell):
    def __init__(self, coordinates: tuple, fuel_moisture: float) -> None:
        super().__init__("grass", coordinates, 0.6, fuel_moisture, 0.3)
    

# road cell
class Road(Cell):
    def __init__(self, coordinates: tuple) -> None:
        super().__init__("road", coordinates, 0, 1, 1)
    
    def prob_spread(self, ambient_humidity, wind_speed, wind_direction, fire_spread_direction):
        return 0


# water cell
class Water(Cell):
    def __init__(self, coordinates: tuple) -> None:
        super().__init__("water", coordinates, 0, 1, 1)

    def prob_spread(self, ambient_humidity, wind_speed, wind_direction, fire_spread_direction):
        return 0




"""
The following cells are building cells. These include aditional fields such as the number of floors in a building in order to more realistically 
keep track of damage caused. Additionally, randomness will be added in the cost_per_sqft field. This is to model the inherent
differences in cost from building to building, even of the same type. There will be upper and lower bounds for each building.
"""

class Building(Cell):

    #floor area is to be given in square feet
    def __init__(self, cell_type: str, 
                 coordinates: tuple, 
                 base_flammability: float, 
                 fuel_moisture: float, 
                 moisture_ext: float,
                 floor_area: float,
                 num_floors: int,
                 cost_per_sqft: int) -> None:
        super().__init__(cell_type, coordinates, base_flammability, fuel_moisture, moisture_ext)
        self.floor_area = floor_area
        self.num_floors = num_floors
        self.cost_per_sqft = cost_per_sqft
    
    #overides cost above
    def cost(self) -> float:
        return self.cost_per_sqft * self.floor_area * self.num_floors
    


# RESIDENTIAL BUILDINGS

# TIMBER HOUSE
# Cost Per Square Foot: 40 - 60
class Shack(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Shack", coordinates, 0.08, fuel_moisture, 0.35, floor_area, num_floors, random.randint(40, 60))


# CONCRETE HOUSE
# Cost Per Square Foot: 100 - 250
class ConcreteHome(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Concrete House", coordinates, 0.04, fuel_moisture, 0.2, floor_area, num_floors, random.randint(100, 250))

# MANSION
# Cost Per Square Foot: 400 - 600
class Mansion(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Mansion", coordinates, 0.05, fuel_moisture, 0.32, floor_area, num_floors, random.randint(400, 600))

# APARTMENT COMPLEX
# Cost Per Square Foot: 150 - 700
class ApartmentComplex(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Apartment Complex", coordinates, 0.06, fuel_moisture, 0.22, floor_area, num_floors, random.randint(150, 700))



#COMMERCIAL BUILDINGS

# OFFICE BUILDING
# Cost Per Square Foot: 240 - 1000
class Office(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Office", coordinates, 0.05, fuel_moisture, 0.18, floor_area, num_floors, random.randint(240, 1000))

# WAREHOUSE
# Cost Per Square Foot: 35 - 150
class Warehouse(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Warehouse", coordinates, 0.07, fuel_moisture, 0.25, floor_area, num_floors, random.randint(35, 150))

# Shopping Mall
# Cost Per Square Foot: 300 - 550
class Mall(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Shopping Mall", coordinates, 0.06, fuel_moisture, 0.2, floor_area, num_floors, random.randint(300, 550))

# Strip Mall
# Cost Per Square Foot: 250 - 470
class StripMall(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Strip Mall", coordinates, 0.08, fuel_moisture, 0.28, floor_area, num_floors, random.randint(250, 470))

# Farm Barn
# Cost Per Square Foot: 15 - 100
class Barn(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Barn", coordinates, 0.16, fuel_moisture, 0.40, floor_area, num_floors, random.randint(15, 100))



#Critical Infrastructure (e.g. fire station, hospital)
# Cost Per Square Foot: 400 - 1000
class Infra(Building) :
    def __init__(self, coordinates: tuple, fuel_moisture: float, floor_area: float, num_floors: int):
        super().__init__("Infrastructure", coordinates, 0.02, fuel_moisture, 0.12, floor_area, num_floors, random.randint(400, 1000))