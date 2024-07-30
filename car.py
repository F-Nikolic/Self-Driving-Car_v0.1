import pygame
import math
from sensor import Sensor
from utils import Utils
from controls import Controls
from neuralNet import NeuralNetwork

class Car:
    """
    Class that initiates and manages the car object. 

    Args:
        x (int): The x coordinate of the car on the screen
        y (int): The y coordinate of the car on the screen
        width (int): The width of the car
        height (int): The height of the car
        control_type (str): The type of car (DUMMY/AGENT)
        max_speed (int): The max speed the car can go; by default 3

    Attributes:
        x (int): The x coordinate of the car on the screen
        y (int): The y coordinate of the car on the screen
        width (int): The width of the car
        height (int): The height of the car
        control_type (str): The type of car (DUMMY/AGENT)
        image (Surface): The surface of the car
        speed (int): The current speed of the car
        acceleration (int): The acceleration of the car
        max_speed (int): The max speed the car can go; by default 3
        friction (int): The friction of car
        angle (int): The current angle of the car
        roation_speed (int): The speed by which the car can rotate
        damaged (bool): If the car is damaged/has crashed or not
        use_brain (bool): If our car is an agent it will drive itself instead of letting the user drive
        controls (Controls): The controls of the car

        sensor (Sensor): ONLY IF THE CAR IS NOT A "DUMMY" CAR
        brain (NeuralNetwork): ONLY IF THE CAR IS AN "AGENT" CAR
    """

    def __init__(self, x, y, width, height, control_type, max_speed = 3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.control_type = control_type

        self.speed = 0
        self.acceleration = 0.5
        self.max_speed = max_speed
        self.friction = 0.05
        self.angle = 0
        self.rotation_speed = 2

        self.damaged = False

        self.use_brain = False

        self.controls = Controls(control_type)

        if control_type == "AGENT":
            self.sensor = Sensor(self)
            self.use_brain = True
            self.brain = NeuralNetwork(
                [self.sensor.ray_count, 6, 4]
            )

    def update(self, road_borders, traffic):
        """
        Updates the car on every frame by checking if it is damaged and if not then creating its polygon and moving it.
        If the car has sensors then it also updates its sensors on every frame as well as sending the
        offsets of the detections as signals to the neural network to receive the outputs and moving the car

        Args:
            road_borders (list): List of the borders on the road
            traffic (list): List of the traffic cars on the road
        """

        if not self.damaged:
            self.move()
            self.polygon = self.create_polygon()
            self.damaged = self.check_damaged(road_borders, traffic)
        else:
            self.speed = 0
        self.controls.handle_controls()

        if hasattr(self, 'sensor'):
            self.sensor.update(road_borders, traffic)

            # Get the offsets and send them as signals to the neural network
            offsets = [0 if x is None else 1 - x["offset"] for x in self.sensor.detections] # If object is far away, neurons receive low values and higher values close to 1 if the object is close 
            # Feed forward the signals and receive proper outputs to control the car
            outputs = NeuralNetwork.feed_forward(offsets, self.brain)

            # If the car is an agent then control the car using the received outputs from the NN
            if self.use_brain:
                self.controls.forward = outputs[0]
                self.controls.left = outputs[1]
                self.controls.right = outputs[2]
                self.controls.reverse = outputs[3]

    def check_damaged(self, road_borders, traffic):
        """
        Checks for collisions of the agent car with other traffic cars and the road border

        Args:
            road_borders (list): List of the borders on the road
            traffic (list): List of the traffic cars on the road

        Returns:
            bool: True if there is an collision
            bool: False if there is none
        """

        for border in road_borders:
            if Utils.polys_intersect(self.polygon, border):
                return True
        for traffic_car in traffic:
            if Utils.polys_intersect(self.polygon, traffic_car.polygon):
                return True
        return False

    def create_polygon(self):
        """
        Calculates and stores the corner points of the car to create the polygon. Used later for calculating intersections and drawing the car

        Returns:
            list: The corner points of the car polygon
        """

        points = []
        rad = math.hypot(self.width, self.height)/2 # Since the car is a rectangle we can simply get the hypothenuse and half it to get the "radius" from the center to each corner
        alpha = math.atan2(self.width, self.height) 

        # The x and v values of the cars position when creating in pygame are not centered so we center it here seperately to make calculations easier
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
        
    def draw(self, screen, new_color, draw_sensor=False):
        '''
        Draws the car on the screen using its corner points, as well as the sensors if the car has them

        Args:
            screen (Surface): The surface to draw the car on
        '''

        color = new_color
        if self.damaged:
            color = (255, 0, 0, 128)
    
        poly_points = [
            (self.polygon[0]["x"], self.polygon[0]["y"]), 
            (self.polygon[1]["x"], self.polygon[1]["y"]),
            (self.polygon[2]["x"], self.polygon[2]["y"]),
            (self.polygon[3]["x"], self.polygon[3]["y"])
            ]
        
        pygame.draw.polygon(screen, color, poly_points) 

        if hasattr(self, 'sensor') and draw_sensor: 
            self.sensor.draw(screen)
        
    def move(self):
        """
        Moves and rotates the car based on the controls by updating its position and speed
        """

        # Accelerates the car 
        if self.controls.forward:
            self.speed += self.acceleration
        if self.controls.reverse:
            self.speed -= self.acceleration

        # Caps the speed
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed/2:
            self.speed = -self.max_speed/2

        # Adds friction
        if self.speed > 0:
            self.speed -= self.friction
        if self.speed < 0:
            self.speed += self.friction
        if abs(self.speed) < self.friction: # Solves the car always moving forward by a small amount  
            self.speed = 0

        # Calculates the rotation angle
        if self.speed != 0:
            flip = 1 if self.speed > 0 else -1
            if self.controls.left:
                self.angle += self.rotation_speed*flip
            if self.controls.right:
                self.angle -= self.rotation_speed*flip

        # Updates the position of the car based on angle and speed
        self.x -= math.sin(math.radians(self.angle))*self.speed

        # Moves the dummy car by updating its y position
        # If we update it for the agents main car too then the car could move out of the screen so we essentially lock the y position for it
        #if self.control_type == "DUMMY":
        self.y -= math.cos(math.radians(self.angle))*self.speed 


        