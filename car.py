import pygame
import math
from sensor import Sensor
from utils import Utils
from controls import Controls

class Car:
    def __init__(self, x, y, width, height, color, control_type, max_speed = 3):
        self.x = x
        self.y = y
        self.fixed_y = y
        self.width = width
        self.height = height
        self.color = color
        self.control_type = control_type
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)

        self.speed = 0
        self.acceleration = 0.5
        self.max_speed = max_speed
        self.friction = 0.05
        self.angle = 0
        self.rotation_speed = 2

        self.damaged = False

        self.controls = Controls(control_type)
        self.sensor = Sensor(self)

    def update(self, road_borders):
        if not self.damaged:
            self.move()
            self.polygon = self.create_polygon()
            self.damaged = self.check_damaged(road_borders)
        else:
            self.speed = 0
        self.controls.handle_controls()
        self.sensor.update(road_borders)

    def check_damaged(self, road_borders):
        for border in road_borders:
            if Utils.polys_intersect(self.polygon, border):
                return True
        return False

    def create_polygon(self):
        points = []
        rad = math.hypot(self.width, self.height)/2
        alpha = math.atan2(self.width, self.height)

        x_center = self.x + self.width/2
        y_center = self.y + self.height/2

        points.append(
            {"x":x_center - math.sin(math.radians(self.angle)-alpha)*rad, 
             "y":y_center - math.cos(math.radians(self.angle)-alpha)*rad}
        )
        points.append(
            {"x":x_center - math.sin(math.radians(self.angle)+alpha)*rad, 
             "y":y_center - math.cos(math.radians(self.angle)+alpha)*rad}
        )
        points.append(
            {"x":x_center - math.sin(math.pi+math.radians(self.angle)-alpha)*rad, 
             "y":y_center - math.cos(math.pi+math.radians(self.angle)-alpha)*rad}
        )
        points.append(
            {"x":x_center - math.sin(math.pi+math.radians(self.angle)+alpha)*rad, 
             "y":y_center - math.cos(math.pi+math.radians(self.angle)+alpha)*rad}
        )
        return points
        
    def draw(self, screen):
        '''
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(rotated_image, new_rect)
        '''

        if self.damaged:
            self.color = (255, 0, 0)
    
        poly_points = [
            (self.polygon[0]["x"], self.polygon[0]["y"]), 
            (self.polygon[1]["x"], self.polygon[1]["y"]),
            (self.polygon[2]["x"], self.polygon[2]["y"]),
            (self.polygon[3]["x"], self.polygon[3]["y"])
            ]
        
        pygame.draw.polygon(screen, self.color, poly_points)

        self.sensor.draw(screen)
        
    def move(self):
        if self.controls.forward:
            self.speed += self.acceleration
        if self.controls.reverse:
            self.speed -= self.acceleration

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed/2:
            self.speed = -self.max_speed/2

        if self.speed > 0:
            self.speed -= self.friction
        if self.speed < 0:
            self.speed += self.friction
        if abs(self.speed) < self.friction: # Solves the car always moving forward by a small amount  
            self.speed = 0

        if self.speed != 0:
            flip = 1 if self.speed > 0 else -1
            if self.controls.left:
                self.angle += self.rotation_speed*flip
            if self.controls.right:
                self.angle -= self.rotation_speed*flip

        self.x -= math.sin(math.radians(self.angle))*self.speed
        #self.y -= math.cos(math.radians(self.angle))*self.speed 


        