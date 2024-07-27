import pygame
import sys
from car import Car
from road import Road

pygame.init()

# Screen settings
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 900
SCREEN_BGCOLOR = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Self Driving Car Simulation")

# Car
car = Car(450, 600, 50, 80, (255, 0, 0))

# Road
ROAD_WIDTH = SCREEN_WIDTH/3
road = Road((SCREEN_WIDTH - ROAD_WIDTH) // 2, ROAD_WIDTH, SCREEN_HEIGHT, 3)


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    car.move(keys_pressed)

    screen.fill(SCREEN_BGCOLOR)

    road.draw(screen)
    car.draw(screen)

    pygame.display.flip()

    clock.tick(60)

# Quit program
pygame.quit
sys.exit()


