import pygame

class Button:
    """
    Button class that creates button objects

    Args:
        text (str): The text on the button
        x (int): The x coordinate of the button
        y (int): The y coordinate of the button
        width (int): The width of the button
        height (int): The height of the button
        callback (method): The method hooked to the button

    Attributes:
        text (str): The text on the button
        x (int): The x coordinate of the button
        y (int): The y coordinate of the button
        width (int): The width of the button
        height (int): The height of the button
        callback (method): The method hooked to the button
    """

    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color = (200, 200, 200)

    def draw(self, screen):
        """
        Draws the button on the screen

        Args:
            screen (Surface): The surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        self.color = (200, 200, 200)

    def handle_event(self, event):
        """
        Handles mouse click events

        Args:
            event (event): The type of event
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                self.color = (0, 255, 0)