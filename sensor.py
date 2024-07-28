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

    def update(self):
        self.cast_rays()

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
            line_width = 2
            pygame.draw.line(screen, (255, 255, 0), (self.rays[i][0]["x"], self.rays[i][0]["y"]), (self.rays[i][1]["x"], self.rays[i][1]["y"]), line_width)