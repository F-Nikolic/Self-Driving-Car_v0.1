import pygame
from utils import Utils

class Road:
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

        top_left = {"x":self.left, "y":self.top}
        top_right = {"x":self.right, "y":self.top}
        bottom_left = {"x":self.left, "y":self.bottom}
        bottom_right = {"x":self.right, "y":self.bottom}
        
        self.borders = [
            [top_left, bottom_left],
            [top_right, bottom_right]
        ] 

    def get_lane_center(self, lane_index, car_size):
        lane_width = self.width/self.lane_count
        return (self.left + lane_width/2 + min(lane_index, self.lane_count-1) * lane_width)-car_size/2

    def draw(self, screen):
        line_width = 5
        pygame.draw.rect(screen, (169, 169, 169), (self.x, 0, self.width, self.height))
       

        for i in range(self.lane_count + 1):
            x = Utils.lerp(
                self.left, 
                self.right,
                i / self.lane_count
            )
            y = 0
            if i > 0 and i < self.lane_count:
                while y < self.height:
                    pygame.draw.line(screen, (255, 255, 255), (x, y), (x, y + 20), line_width)
                    y += 40
            else:
                pygame.draw.line(screen, (255, 255, 255), (x, self.top), (x, self.bottom), line_width)




