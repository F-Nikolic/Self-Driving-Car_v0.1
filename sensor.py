import pygame
import math
from utils import Utils

class Sensor:
    def __init__(self, car):
        self.car = car
        self.ray_count = 5
        self.ray_length = 150
        self.ray_spread = math.pi/2

        self.rays = []
        self.detections = []

    def update(self, road_borders, traffic):
        self.cast_rays()
        self.detections = []
        for ray in self.rays:
            self.detections.append(
                self.get_reading(ray, road_borders, traffic)
            )

    def get_reading(self, ray, road_borders, traffic):
        collisions = []

        for border in road_borders:
            collision = Utils.get_intersection(
                ray[0], 
                ray[1],
                border[0],
                border[1]
            )
            if collision:
                collisions.append(collision)

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
            #offsets = map(lambda x: x.offset, collisions)
            #smallest_offset = min(collisions, key=lambda x: x.offset).offset

    def cast_rays(self):
        self.rays = []
        for i in range(self.ray_count):
            ray_angle = Utils.lerp(
                self.ray_spread / 2, 
                -self.ray_spread / 2, 
                i / (self.ray_count-1) if self.ray_count != 1 else 0.5
            )+math.radians(self.car.angle)

            start = {"x":self.car.x+(self.car.width/2), "y":self.car.y+(self.car.height/2)}
            end = {"x":(self.car.x+(self.car.width/2)) - math.sin(ray_angle) * self.ray_length, 
                   "y":self.car.y - math.cos(ray_angle) * self.ray_length}
            
            self.rays.append([start, end])
        
    def draw(self, screen):
        for i in range(self.ray_count):
            end = self.rays[i][1]
            if self.detections[i]:
                end = self.detections[i]
                
            line_width = 2
            pygame.draw.line(screen, (0, 0, 0), (self.rays[i][0]["x"], self.rays[i][0]["y"]), (self.rays[i][1]["x"], self.rays[i][1]["y"]), line_width)
            pygame.draw.line(screen, (255, 255, 0), (self.rays[i][0]["x"], self.rays[i][0]["y"]), (end["x"], end["y"]), line_width)