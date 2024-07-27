import pygame

class Car:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)

    def draw(self, screen):
        screen.blit(self.image, 
            (self.x - self.width/2, 
             self.y - self.height/2))
        
    def move(self, keysPressed):
        if keysPressed[pygame.K_w]:
            self.y -= self.speed
        if keysPressed[pygame.K_s]:
            self.y += self.speed
        if keysPressed[pygame.K_a]:
            self.x -= self.speed
        if keysPressed[pygame.K_d]:
            self.x += self.speed


        