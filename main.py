import pygame
import sys
import random
from car import Car
from road import Road
from neuralNet import NeuralNetwork

def main():
    """
    The main function that initializes the game, sets up the screen and objects, and runs the game loop.
    """

    pygame.init()

    # car screen settings
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1100
    SCREEN_BGCOLOR = (100, 100, 100)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Self Driving Car Simulation")

    # Road instance
    ROAD_WIDTH = SCREEN_WIDTH/3
    ROAD_CENTER = 50
    LINE_CENTER = ROAD_WIDTH/2 + ROAD_CENTER
    road = Road(ROAD_CENTER, ROAD_WIDTH, LINE_CENTER, SCREEN_HEIGHT, 3)

    # Car agent instances
    n = 100
    cars = generate_cars(n, road, "AGENT")

    # Traffic instance
    traffic = [
        #Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), "DUMMY"),
        #Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), "DUMMY"),
    ]

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False
                    main()

        for traffic_car in traffic:
            traffic_car.update(road.borders,[])

        for agent_car in cars:
            agent_car.update(road.borders, traffic)

        road.scroll_speed = cars[0].speed

        screen.fill(SCREEN_BGCOLOR)

        road.draw(screen)

        for traffic_car in traffic:
            traffic_car.y += road.scroll_speed # Simulates overtaking effect by adjusting the traffic cars y position relevant to the scroll speed
            traffic_car.draw(screen)
        for agent_car in cars:
            agent_car.draw(screen)

        # Debug and visualization for the neural network
        NeuralNetwork.draw_debug(screen, ROAD_WIDTH+70, SCREEN_WIDTH/1.75, SCREEN_HEIGHT, cars[0].brain)

        pygame.display.flip()

        clock.tick(60)

    # Quit program
    pygame.quit
    sys.exit()

def generate_cars(n, road, car_type):
    """
    Generates n amount of cars

    Args:
        n (int): The amount of cars to be generated
        road (Road): The road of the simulation
        car_type (str): Type of car to generate (DUMMY/AGENT)

    Returns:
        list: The cars in the traffic
    """

    cars = []
    for i in range(n+1):

        if car_type == "DUMMY":
            cars.append(Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), "DUMMY"))
        elif car_type == "AGENT":
            cars.append(Car(road.get_lane_center(0, 30), 600, 30, 50, (0, 255, 0, 200), "AGENT", 5))
    
    return cars

if __name__ == '__main__':
    main()


