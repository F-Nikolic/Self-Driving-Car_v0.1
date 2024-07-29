import pygame

class Controls:
    def __init__(self, control_type):
        self.forward = False
        self.left = False
        self.right = False
        self.reverse = False
        self.control_type = control_type

    def handle_controls(self):
        if self.control_type == "AGENT":
            keys_pressed = pygame.key.get_pressed() 

            if keys_pressed[pygame.K_w]:
                self.forward = True
            if keys_pressed[pygame.K_s]:
                self.reverse = True
            if keys_pressed[pygame.K_a]:
                self.left = True
            if keys_pressed[pygame.K_d]:
                self.right = True
            self.reset_controls(keys_pressed)
        else:
             self.forward = True

    def reset_controls(self, keys_pressed):
        self.forward = True if keys_pressed[pygame.K_w] else False
        self.left = True if keys_pressed[pygame.K_a] else False
        self.right = True if keys_pressed[pygame.K_d] else False
        self.reverse = True if keys_pressed[pygame.K_s] else False