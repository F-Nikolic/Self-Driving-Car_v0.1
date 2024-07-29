import pygame
import sys
from car import Car
from road import Road

pygame.init()

# Screen settings
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 900
SCREEN_BGCOLOR = (100, 100, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Self Driving Car Simulation")

# Road
ROAD_WIDTH = SCREEN_WIDTH/3
ROAD_CENTER = (SCREEN_WIDTH - ROAD_WIDTH)//2
LINE_CENTER = SCREEN_WIDTH/2
road = Road(ROAD_CENTER, ROAD_WIDTH, LINE_CENTER, SCREEN_HEIGHT, 3)

# Car
car = Car(road.get_lane_center(0, 30), 600, 30, 50, (0, 255, 0))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    car.update(keys_pressed, road.borders)

    road.scroll_speed = car.speed

    screen.fill(SCREEN_BGCOLOR)

    road.draw(screen)
    car.draw(screen)

    pygame.display.flip()

    clock.tick(60)

# Quit program
pygame.quit
sys.exit()


