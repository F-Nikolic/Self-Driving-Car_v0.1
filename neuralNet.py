import random
import pygame
from visualizer import Visualizer

class NeuralNetwork:
    def __init__(self, neuron_counts):
        self.levels = []

        for i in range(len(neuron_counts)-1):
            self.levels.append(Level(
                neuron_counts[i], neuron_counts[i+1]
            ))

    def feed_forward(given_inputs, network):
        outputs = Level.feed_forward(
            given_inputs, network.levels[0])
        
        for i in range(1, len(network.levels)):
            outputs = Level.feed_forward(
                outputs, network.levels[i]
            )
        return outputs
    
    def draw_debug(screen, x, width, height, network):
        pygame.draw.rect(screen, (0, 0, 0), (x, 0, width, height))
        Visualizer.draw_network(screen, network)
        
      
class Level:
    def __init__(self, input_count, output_count):
        self.inputs = [None for _ in range(input_count)]
        self.outputs = [None for _ in range(output_count)]
        self.biases = [None for _ in range(output_count)]

        self.weights = [[None for _ in range(output_count)] for _ in range(input_count)] # For each input node we have #output_count connections
        
        Level.randomize(self)

    def randomize(level):
        for i in range(len(level.inputs)):
            for j in range(len(level.outputs)): 
                level.weights[i][j] = random.uniform(-1, 1) # Negative values to help decide which way to turn 
        
        for i in range(len(level.biases)):
            level.biases[i] = random.uniform(-1, 1)

    def feed_forward(given_inputs, level):
        for i in range(len(level.inputs)):
            level.inputs[i] = given_inputs[i]
        
        for i in range(len(level.outputs)):
            sum = 0
            for j in range(len(level.inputs)):
                sum += level.inputs[j]*level.weights[j][i]
            
            if sum > level.biases[i]:
                level.outputs[i] = 1 # Turn on the output neuron because the sum of the signals is bigger than the bias
            else:
                level.outputs[i] = 0 # turn off the output neuron

        return level.outputs