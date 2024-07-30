import pygame
from utils import Utils

class Visualizer:
    def draw_network(screen, network):
        margin = 50
        left = margin
        top = margin
        screen_width, screen_height = screen.get_size()
        width = screen_width-margin*2
        height = screen_height-margin*2

        level_height = height / len(network.levels)

        for i in range(len(network.levels) - 1, -1, -1):
            level_top = top + Utils.lerp(
                    height - level_height,
                    0,
                    0.5 if len(network.levels) == 1 else i / (len(network.levels) - 1)
                )

            Visualizer.drawLevel(
                screen,
                network.levels[i],
                left,
                level_top,
                width,
                level_height,
                ['W','A','D','S'] if i == len(network.levels) - 1 else [])

    def drawLevel(screen, level, left, top, width, height, output_labels):
        right = left + width
        bottom = top + height

        inputs, outputs, weights, biases = level.inputs, level.outputs, level.weights, level.biases

        for i in range(len(inputs)):  
            for j in range(len(outputs)):  
                pygame.draw.line(screen, get_RGB(weights[i][j]), 
                                 (Visualizer.get_node_X(inputs,i,left,right), bottom), 
                                 (Visualizer.get_node_X(inputs,i,left,right), top), 2)
        
        node_radius=18
        for i in range(len(inputs)):  
            x = Visualizer.get_node_X(inputs,i,left,right);
            
            pygame.draw.circle(screen, (0, 0, 0), (x, bottom), node_radius)
            pygame.draw.circle(screen, get_RGB(inputs[i]), (x, bottom), node_radius*0.6)
        
        for i in range(len(outputs)): 
            x = Visualizer.get_node_X(outputs,i,left,right);
            pygame.draw.circle(screen, (0, 0, 0), (x, top), node_radius)
            pygame.draw.circle(screen, get_RGB(outputs[i]), (x, top), node_radius*0.6)

            pygame.draw.circle(screen, get_RGB(biases[i]), (x, top), node_radius*0.8)
         
            if output_labels and i < len(output_labels):
                if output_labels[i]:
                    # Set up the font
                    font_size = round(node_radius*1.5)
                    font = pygame.font.Font(None, font_size)  # None uses the default font

                    # Render the text
                    text = output_labels[i]
                    text_surface = font.render(text, True, (0, 0, 0))  # True for anti-aliasing

                    # Get the text rectangle and position it
                    text_rect = text_surface.get_rect()
                    text_rect.center = (x, top)
                    screen.blit(text_surface, text_rect)


 
    def get_node_X(nodes, index, left, right):
        return Utils.lerp(
            left,
            right,
            0.5 if len(nodes) == 1 else index/(len(nodes)-1))
           

def get_RGB(value):
    R = 0 if value < 0 else 255
    G = R
    B = 0 if value > 0 else 255
    return (R, G, B)
