import pygame
import sys
import random
from car import Car
from road import Road

def main():
    """
    The main function that initializes the game, sets up the screen and objects, and runs the game loop.
    """

    pygame.init()

    # Screen settings
    SCREEN_HEIGHT = 700
    SCREEN_WIDTH = 900
    SCREEN_BGCOLOR = (100, 100, 100)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self Driving Car Simulation")

    # Road instance
    ROAD_WIDTH = SCREEN_WIDTH/3
    ROAD_CENTER = (SCREEN_WIDTH - ROAD_WIDTH)//2
    LINE_CENTER = SCREEN_WIDTH/2
    road = Road(ROAD_CENTER, ROAD_WIDTH, LINE_CENTER, SCREEN_HEIGHT, 3)

    # Car agent instance
    car = Car(road.get_lane_center(0, 30), 600, 30, 50, (0, 255, 0), "AGENT", 5)

    # Traffic instance
    traffic = [
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), "DUMMY"),
    ]

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for traffic_car in traffic:
            traffic_car.update(road.borders,[])

        car.update(road.borders, traffic)

        road.scroll_speed = car.speed

        screen.fill(SCREEN_BGCOLOR)

        road.draw(screen)

        for traffic_car in traffic:
            traffic_car.y += road.scroll_speed # Simulates overtaking effect by adjusting the traffic cars y position relevant to the scroll speed
            traffic_car.draw(screen)

        car.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    # Quit program
    pygame.quit
    sys.exit()

if __name__ == '__main__':
    main()


