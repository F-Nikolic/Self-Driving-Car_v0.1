import pygame
import math
from utils import Utils

class Sensor:
    """
    Class responsible for adding sensors to the agent car

    Args:
        car (Car): The agents car 
    
    Attributes:
        car (Car): The car object that receives the sensors
        ray_count (int): Amount of rays
        ray_length (int): How far the sensors reach
        ray_spread (int): The angle between each ray
        rays (list): List that stores all rays for the sensor
        detections (list): List that stores all readings from the sensor, usually being the minimum offsets from the ray to the obstacle
    """
    def __init__(self, car):
        self.car = car
        self.ray_count = 5
        self.ray_length = 150
        self.ray_spread = math.pi/2

        self.rays = []
        self.detections = []

    def update(self, road_borders, traffic):
        """
        Updates the sensors every frame by checking if there are any readings

        Args:
            road_borders (list): List of the borders of the road
            traffic (list): List of the traffic cars on the road
        """
        self.cast_rays()
        self.detections = []
        # Go through every ray and check if there are any readings
        for ray in self.rays:
            self.detections.append(
                self.get_reading(ray, road_borders, traffic)
            )

    def get_reading(self, ray, road_borders, traffic):
        """
        Helper method checking for readings and detecting collision using the get_intersection() method from the utils class

        Args:
            ray (list): Line segment of the ray containing the start and end point
            road_borders (list): List of the borders of the road
            traffic (list): List of the traffic cars on the road

        Returns:
            none: If there are no collisions
            int: The smallest offset of the collision with the ray and the obstacle
        """

        collisions = []

        # Checking for readings on the border
        # Goes through every segment of the border and checks for intersections with the ray segment
        for border in road_borders:
            collision = Utils.get_intersection(
                ray[0], 
                ray[1],
                border[0],
                border[1]
            )
            if collision:
                collisions.append(collision)

        # Checking for readings on the traffic cars
        # Goes through every segment of the traffic car and checks for intersections with the ray segment
        for traffic_car in traffic:
            poly = traffic_car.polygon
            for i in range(len(poly)):
                collision = Utils.get_intersection(
                    ray[0], 
                    ray[1],
                    poly[i],
                    poly[(i+1)%len(poly)] 
                )
                if collision:
                    collisions.append(collision)

        if len(collisions) == 0:
            return None
        else:
            return min(collisions, key=lambda x: x["offset"]) #returns the collision with the smallest offset

    def cast_rays(self):
        """
        "Casts" a ray by creating segments using calculated start and end points
        """

        self.rays = []
        for i in range(self.ray_count):
            # Get the angle of the ray by linear interpolation and adding the car angle to it
            ray_angle = Utils.lerp(
                self.ray_spread / 2, 
                -self.ray_spread / 2, 
                i / (self.ray_count-1) if self.ray_count != 1 else 0.5
            )+math.radians(self.car.angle)

            start = {"x":self.car.x+(self.car.width/2), "y":self.car.y+(self.car.height/2)} # Originate the ray from the center of the car
            end = {"x":(self.car.x+(self.car.width/2)) - math.sin(ray_angle) * self.ray_length, # Use the pre-defined attributes and the ray angle to determine where the ray "casts" to
                   "y":self.car.y - math.cos(ray_angle) * self.ray_length} 
            
            self.rays.append([start, end])
        
    def draw(self, screen):
        """
        Draws each ray on the given surface

        Args:
            screen (surface): The surface to draw on
        """

        for i in range(self.ray_count):
            end = self.rays[i][1]
            if self.detections[i]:
                end = self.detections[i] # Sets the end point to the collisions position, else it remains the max reach
                
            line_width = 2
            pygame.draw.line(screen, (0, 0, 0), (self.rays[i][0]["x"], self.rays[i][0]["y"]), (self.rays[i][1]["x"], self.rays[i][1]["y"]), line_width) # Draws and colors the sensors black beyond the collision if there is any
            pygame.draw.line(screen, (255, 255, 0), (self.rays[i][0]["x"], self.rays[i][0]["y"]), (end["x"], end["y"]), line_width) # Draws and colors the sensors yellow up until the end point
