import pygame

class Road:
    def __init__(self, x, width, height, lane_count):
        self.x = x
        self.width = width
        self.height = height

        self.lane_count = lane_count
        self.dash_length = 20
        self.dash_gap = 20


    def draw(self, screen):
        pygame.draw.rect(screen, (169, 169, 169), (self.x, 0, self.width, self.height))

        for i in range(1, self.lane_count):
            lane_x = self.x + i * 100
            y = 0 % (self.dash_length + self.dash_gap)
            while y < self.height:
                pygame.draw.line(screen, (255, 255, 255), (lane_x, y), (lane_x, y + self.dash_length), 5)
                y += self.dash_length + self.dash_gap

