import pygame
from utils import Utils

class Visualizer:
    """
    Class responsible for visualizing the network during runtime by updating on every frame
    """

    def draw_network(screen, network, width, nn_screen_left):
        """
        Draws the neural network 

        Args:
            screen (Surface): The surface to draw the object on
            network (NeuralNetwork): The neural network which is going to be drawn
            width (int): The width of the screen for the visualization
            nn_screen_left (int): The starting point of the screen for the network
        """

        margin = 50
        left = nn_screen_left
        top = margin
        screen_width, screen_height = screen.get_size()
        height = screen_height-margin*2

        # Determine level height
        level_height = height / len(network.levels)

        for i in range(len(network.levels) - 1, -1, -1):
            # Determine level top by interpolating through the whole level hight
            level_top = top + Utils.lerp(
                    height - level_height,
                    0,
                    0.5 if len(network.levels) == 1 else i / (len(network.levels) - 1)
                )

            # Draw each level of the network
            Visualizer.drawLevel(
                screen,
                network.levels[i],
                left,
                level_top,
                width,
                level_height,
                ['W','A','D','S'] if i == len(network.levels) - 1 else [])

    def drawLevel(screen, level, left, top, width, height, output_labels):
        """
        Draws the the nodes and lines of the specific level

        Args:
            screen (Surface): The surface to draw the object on
            level (list): The level being drawn
            left (int): The starting node of each level on the furthest left
            top (int): The top of the current level
            width (int): The width of the screen for the visualization
            height (int): The height of the level 
            output_labels (list): The labels of the output nodes (here being the letters of the control keys or nothing if the output node is on a hidden layer)
        """

        right = left + width
        bottom = top + height

        inputs, outputs, biases, weights = level.inputs, level.outputs, level.biases, level.weights

        # Draw all lines
        for i in range(len(inputs)):  
            for j in range(len(outputs)):  
                start_pos = (Visualizer.get_node_X(inputs,i,left,right), bottom)
                end_pos = (Visualizer.get_node_X(outputs,j,left,right), top)
                draw_dashed_line(screen, get_RGB(weights[i][j]), start_pos, end_pos, 7, 3)
        
        node_radius=18
        # Draw the input nodes
        for i in range(len(inputs)):  
            x = Visualizer.get_node_X(inputs,i,left,right);
            
            pygame.draw.circle(screen, (0, 0, 0), (x, bottom), node_radius)
            pygame.draw.circle(screen, get_RGB(inputs[i]), (x, bottom), node_radius*0.8)
        
        # Draw the output nodes, including the hidden layers
        for i in range(len(outputs)): 
            x = Visualizer.get_node_X(outputs,i,left,right);
            pygame.draw.circle(screen, (0, 0, 0), (x, top), node_radius*1.2)
            pygame.draw.circle(screen, get_RGB(outputs[i]), (x, top), node_radius)
            #pygame.draw.circle(screen, get_RGB(biases[i]), (x, top), node_radius)
         
            # Write the label on the output node
            if output_labels and i < len(output_labels):
                if output_labels[i]:
                    font_size = round(node_radius*1.5)
                    font = pygame.font.Font(None, font_size) 

                    text = output_labels[i]
                    text_surface = font.render(text, True, (0, 0, 0)) 

                    text_rect = text_surface.get_rect()
                    text_rect.center = (x, top)
                    screen.blit(text_surface, text_rect)

    def get_node_X(nodes, index, left, right):
        """
        Gets the x position of the node using linear interpolation

        Args:
            nodes (list): List of nodes in the level
            index (int): The node we want the x position to get
            left (int): The starting node's x position of the level
            right (int): The end node's x position of the level
        """

        return Utils.lerp(
            left,
            right,
            0.5 if len(nodes) == 1 else index/(len(nodes)-1))
    
def draw_dashed_line(surface, color, start_pos, end_pos, dash_length, space_length):
    """
    Draws a dashed line on the surface from start_pos to end_pos.
    
    Args:
        surface (pygame.Surface): The surface to draw on.
        color (tuple): The color of the line (R, G, B).
        start_pos (tuple): The starting position of the line (x, y).
        end_pos (tuple): The ending position of the line (x, y).
        dash_length (int): Length of each dash.
        space_length (int): Length of space between dashes.
    """

    # Calculate the total length of the line
    total_length = ((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5

    # Calculate the number of dashes
    num_dashes = int(total_length / (dash_length + space_length))
    
    # Calculate direction vector
    dx = (end_pos[0] - start_pos[0]) / total_length
    dy = (end_pos[1] - start_pos[1]) / total_length
    
    # Draw the dashes
    for i in range(num_dashes):
        start_dash_x = start_pos[0] + i * (dash_length + space_length) * dx
        start_dash_y = start_pos[1] + i * (dash_length + space_length) * dy
        end_dash_x = start_dash_x + dash_length * dx
        end_dash_y = start_dash_y + dash_length * dy
        pygame.draw.line(surface, color, (start_dash_x, start_dash_y), (end_dash_x, end_dash_y), 2)
           
def get_RGB(value):
    """
    Colors the lines and nodes based on the node values

    Args:
        value (int): The value of the node
    """

    a = abs(value)
    G = 0 if value <= 0 else 255
    R = 0 if value > 0 else 255
    B = 0 
    return (R, G, B)
