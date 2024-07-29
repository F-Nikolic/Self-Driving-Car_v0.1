import pygame
from utils import Utils

class Road:
    """
    Class responsible for initiating and drawing the road 

    Args:
        x (int): x start coordinate of the road on the screen representing the center of the road
        width (int): The width of the road
        line_x (int): The center of the road line
        height (int): The height of the road 
        lane_count (int): The amount of lanes the road has; by default 2

    Attributes:
        x (int): The x value for the center of the road
        width (int): The width of the road
        height (int): The height of the road 
        left (int): The x value for the left corner of the road
        right (int): The x value for the right corner of the road
        lane_count (int): The amount of lanes the road has; by default 2
        dash_length (int): The length of the dashed lines for the lanes
        dash_gap (int): The distance between the dashed lines
        infinity (int): A big value to make the road infinitely long
        top (int): Top of the road (y value)
        bottom (int): Bottom of the road (y value)
        scroll (int): How much the road shape scrolls 
        scroll_speed (int): The speed of the scroll
        top_left (dict): The coordinates of the top left corner point of the road
        top_right (dict): The coordinates of the top right corner point of the road
        bottom_right (dict): The coordinates of the bottom right corner point of the road
        bottom_left (dict): The coordinates of the bottom left corner point of the road
        borders (list): List of the corner points of the road
    """
    def __init__(self, x, width, line_x, height, lane_count=2):
        self.x = x
        self.width = width
        self.height = height

        self.left = line_x - width*0.95/2
        self.right = line_x + width*0.95/2

        self.lane_count = lane_count
        self.dash_length = 20
        self.dash_gap = 20

        infinity = 1000000
        self.top = -infinity
        self.bottom = infinity

        self.scroll = 0
        self.scroll_speed = 0

        top_left = {"x":self.left, "y":self.top}
        top_right = {"x":self.right, "y":self.top}
        bottom_left = {"x":self.left, "y":self.bottom}
        bottom_right = {"x":self.right, "y":self.bottom}

        self.borders = [
            [top_left, bottom_left],
            [top_right, bottom_right]
        ] 

    def get_lane_center(self, lane_index, car_size):
        """
        Calculates and returns the center of each lane to position the car on

        Args:
            lane_index (int): The index of the lane where the car is to be positioned (starting at 0)
            car_size (int): Car width 

        Returns:
            int: x position of the car depending on the lane and its width
        """

        lane_width = self.width/self.lane_count
        return (self.left + lane_width/2 + min(lane_index, self.lane_count-1) * lane_width)-car_size/2

    def draw(self, screen):
        """
        Responsible for drawing the road along its lane lines on the screen

        Args:
            screen (Surface): The surface on which to draw the road on
        """
        
        line_width = 5

        # Draws the road itself
        pygame.draw.rect(screen, (169, 169, 169), (self.x, 0, self.width, self.height))
       
       # Draws the dashed lines
        for i in range(self.lane_count + 1):
            # Uses linear interpolation to determine the x value of the dashed lines
            x = Utils.lerp(
                self.left, 
                self.right,
                i / self.lane_count
            )
            y = self.scroll % (self.dash_length + self.dash_gap) - self.dash_length - self.dash_gap
            while y < self.height:
                pygame.draw.line(screen, (255, 255, 255), (x, y), (x, y + self.dash_length), line_width)
                y += self.dash_length + self.dash_gap
        
        # Draws the border lines
        for border in self.borders:
            pygame.draw.line(screen, (255, 255, 255), (border[0]["x"], border[0]["y"]), (border[1]["x"], border[1]["y"]), line_width)

        # Simulates the scroll effect
        self.scroll += self.scroll_speed
        if self.scroll >= self.dash_length + self.dash_gap:
            self.scroll = 0
            
           
            




