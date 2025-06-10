#Insert all cell type objects here
from abc import ABC, abstractmethod
import math

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
        base_prob = 0.5
        return base_prob * self.get_flammability(ambient_humidity) * self.wind_effect(wind_speed, wind_direction, fire_spread_direction)
    

    def compute_weight(self) -> float:
        # calculates the weight of the cell
        # returns a float value
        return 1.0 / self.prob_spread()
    

    def get_coordinates(self):
        return self.coordinates
    
    def __str__(self) -> str:
        return f"Cell(type={self.cell_type}, coordinates={self.coordinates}, base_flammability={self.base_flammability}, fuel_moisture={self.fuel_moisture}, moisture_ext={self.moisture_ext})"
    
    def __repr__(self) -> str:
        return self.__str__()

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
    
    def compute_weight(self):
        return float('inf')


# water cell
class Water(Cell):
    def __init__(self, coordinates: tuple) -> None:
        super().__init__("water", coordinates, 0, 1, 1)

    def prob_spread(self, ambient_humidity, wind_speed, wind_direction, fire_spread_direction):
        return 0
    
    def compute_weight(self):
        return float('inf')

# Materials of buildings
"""
# Abstracted building cell
class Building(Cell):
    def __init__(self, coordinates, fuel_moisture, moisture_ext):
        super().__init__("Buildling", coordinates, 0.3, fuel_moisture, moisture_ext)
"""