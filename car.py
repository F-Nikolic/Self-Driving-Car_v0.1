import pygame
import math
from sensor import Sensor

class Car:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)

        self.speed = 0
        self.acceleration = 0.5
        self.max_speed = 5
        self.friction = 0.05
        self.angle = 0
        self.rotation_speed = 2

        self.sensor = Sensor(self)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(rotated_image, new_rect)

        self.sensor.draw(screen)
        
    def move(self, keysPressed):
        if keysPressed[pygame.K_w]:
            self.speed += self.acceleration
        if keysPressed[pygame.K_s]:
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
            if keysPressed[pygame.K_a]:
                self.angle += self.rotation_speed*flip
            if keysPressed[pygame.K_d]:
                self.angle -= self.rotation_speed*flip

        self.x -= math.sin(math.radians(self.angle))*self.speed
        #self.y -= math.cos(math.radians(self.angle))*self.speed 

        self.sensor.update()

        return self.speed

        