import pygame
import sys
import random
import os
from car import Car
from road import Road
from neuralNet import NeuralNetwork
from buttons import Button

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
    best_car = cars[0]

    #Load model if exists
    if os.path.exists("model.json"):
        for i in range(0, len(cars)):
            NeuralNetwork.load_model(cars[i], "model.json")
        if i != 0:
            NeuralNetwork.mutate(cars[i].brain, 0.1)

    # Traffic instance
    traffic = [
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 800), 30, 50, "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 800), 30, 50, "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 800), 30, 50, "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 800), 30, 50, "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 800), 30, 50, "DUMMY"),
        Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 800), 30, 50, "DUMMY")
    ]
    
    # Button instance
    save_button = Button("Save Model", 0, 0, 200, 50, lambda: NeuralNetwork.save_model(best_car, 'model.json'))
    discard_button = Button("Delete Model", 250, 0, 200, 50, lambda: NeuralNetwork.delete_model('model.json'))

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
            save_button.handle_event(event)
            discard_button.handle_event(event)
                   
        for traffic_car in traffic:
            traffic_car.update(road.borders,[])
        for agent_car in cars:
            agent_car.update(road.borders, traffic)
        
        # Find the minimum y value among all cars
        min_y = min(car.y for car in cars)

        # Find the car(s) with the minimum y value
        best_car = next(car for car in cars if car.y == min_y)

        road.scroll_speed = best_car.speed

        screen.fill(SCREEN_BGCOLOR)

        road.draw(screen)

        for traffic_car in traffic:
            traffic_car.y += road.scroll_speed # Simulates overtaking effect by adjusting the traffic cars y position relevant to the scroll speed
            traffic_car.draw(screen, (0, 0, 255))
        for i in range(1, len(cars)):
            cars[i].y += road.scroll_speed
            cars[i].draw(screen, (255, 255, 0))
        best_car.draw(screen, (0, 255, 0), True)

        save_button.draw(screen)
        discard_button.draw(screen)

        # Debug and visualization for the neural network
        NeuralNetwork.draw_debug(screen, ROAD_WIDTH+70, SCREEN_WIDTH/1.75, SCREEN_HEIGHT, best_car.brain)

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
            cars.append(Car(road.get_lane_center(random.randrange(0, 2), 30), random.randrange(0, 550), 30, 50, "DUMMY"))
        elif car_type == "AGENT":
            cars.append(Car(road.get_lane_center(random.randrange(0, 2), 30), 600, 30, 50, "AGENT", 5))
    
    return cars

if __name__ == '__main__':
    main()


