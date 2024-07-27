import pygame
import math

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
        self.acceleration = 0.2
        self.maxSpeed = 5
        self.friction = 0.05
        self.angle = 0

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(rotated_image, new_rect)
        
    def move(self, keysPressed):
        if keysPressed[pygame.K_w]:
            self.speed += self.acceleration
        if keysPressed[pygame.K_s]:
            self.speed -= self.acceleration

        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        if self.speed < -self.maxSpeed/2:
            self.speed = -self.maxSpeed/2

        if self.speed > 0:
            self.speed -= self.friction
        if self.speed < 0:
            self.speed += self.friction
        if abs(self.speed) < self.friction: # Solves the car always moving forward by a small amount  
            self.speed = 0

        if keysPressed[pygame.K_a]:
            self.angle += 1
        if keysPressed[pygame.K_d]:
            self.angle -= 1

        self.x -= math.sin(math.radians(self.angle))*self.speed
        self.y -= math.cos(math.radians(self.angle))*self.speed


        