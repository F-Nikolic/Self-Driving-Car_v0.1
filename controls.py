import pygame

class Controls:
    """
    Control object that tracks and handles the car agents controls
    
    Args:
        control_type (str): Used to specify if the controls are for a dummy car or the agent car

    Attributes:
        forward (bool): Moves the car forwards
        left (bool): Moves the car to the left
        right (bool): Moves the car to the right
        reverse (bool):  Moves the car backwards
        control_type (str): Specifies if the car is a dummy car of the agent car
    """

    def __init__(self, control_type):
        self.forward = False
        self.left = False
        self.right = False
        self.reverse = False
        self.control_type = control_type

    def handle_controls(self):
        """
        Handles the car controls by checking which keys are pressed 
        on every frame and thus sets the control values accordingly.
        """

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
        """
        Resets the car controls of the keys that are not pressed/released

        Args:
            keys_pressed (bools): Boolean values of every key on the keyboard
        """

        self.forward = True if keys_pressed[pygame.K_w] else False
        self.left = True if keys_pressed[pygame.K_a] else False
        self.right = True if keys_pressed[pygame.K_d] else False
        self.reverse = True if keys_pressed[pygame.K_s] else False