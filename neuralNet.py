import random
import pygame
import json
import os
from visualizer import Visualizer

class NeuralNetwork:
    """
    Class responsible for constructing an artificial neural network

    Args:
        neuron_counts (list): The amount of neurons that the network is going to use.
            Consisting of the input nodes, the hidden layer nodes and the amount of output nodes

    Attributes:
        levels (list): Stores all the levels of the network
    """

    def __init__(self, neuron_counts):
        self.levels = []

        # Creates a level for each input and output layer and appends it to the network
        # i being the input layer and i+1 the output respectively the input for the next layer,
        for i in range(len(neuron_counts)-1):
            self.levels.append(Level(
                neuron_counts[i], neuron_counts[i+1]
            ))

    def feed_forward(given_inputs, network):
        """
        Feeds forward the signal of the input nodes to the output nodes

        Args:
            given_inputs (list) The inputs that are being fed forward, in our case; The offsets detected from the sensors
            network (NeuralNetwork): The specific neural netowrk being used to feed forward the info

        Returns:
            list: A list of the end result with the corresponding output values used to control the car (binary values)
        """

        # Calculates outputs of first level
        outputs = Level.feed_forward(
            given_inputs, network.levels[0])
        
        # Feeds forward and calculates the output of the rest of all levels until reaching the output layer
        for i in range(1, len(network.levels)):
            outputs = Level.feed_forward(
                outputs, network.levels[i]
            )
        return outputs
    
    def draw_debug(screen, x, width, height, network):
        """
        Draws a visualization of the network used for debuging and presentation

        Args:
            screen (Surface): The surface to draw the object on
            x (int): The starting point of the screen on the x axis
            width (int): The width of the screen for the visualization
            height (int): The height of the screen for the visualization
            network (NeuralNetwork): The neural network which is going to be drawn
        """

        pygame.draw.rect(screen, (0, 0, 0), (x, 0, width, height))
        Visualizer.draw_network(screen, network, width, x)

    def save_model(best_car, file_path):
        """
        Saves the training progress of the neural network

        Args:
            best_car (Car): The car with the current neural network
            file_path (str): Path of the json file that stores the model
        """

        model_data = {'levels': []}
        for level in best_car.brain.levels:
            level_data = {
                'inputs': level.inputs,
                'outputs': level.outputs,
                'weights': level.weights,
                'biases': level.biases
            }
            model_data['levels'].append(level_data)
        
        json_string = json.dumps(model_data, indent=4)

        with open(file_path, 'w') as f:
            json.dump(model_data, f)
        print("Saved model!")

    def load_model(best_car, file_path):
        """
        Saves the training progress of the neural network

        Args:
            best_car (Car): The car to load the network in
            file_path (str): Path of the json file that stores the model
        """

        brain = best_car.brain

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                model_data = json.load(f)
            
            for level, level_data in zip(brain.levels, model_data['levels']):
                level.inputs = level_data['inputs']
                level.outputs = level_data['outputs']
                level.weights = level_data['weights']
                level.biases = level_data['biases']
            print(f"Model loaded from '{file_path}'.")
        else:
            print(f"Model file '{file_path}' does not exist.")

    def delete_model(file_path):
        """
        Saves the training progress of the neural network

        Args:
            best_car (Car): The car with the current neural network
            file_path (str): Path of the json file that stores the model
            
        Raises:
            FileNotFoundError: The file does not exist
            Exception: Some other problem occured
        """
        try:
            os.remove(file_path)
            print(f"Model file '{file_path}' has been deleted.")
        except FileNotFoundError:
            print(f"Model file '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while deleting the model file: {e}")
        
      
class Level:
    """
    Class responsible for creating and managing a level object consisting of an input and output layer

    Args:
        input_count (int): The amount of input nodes for the level
        output_count (int): The amount of output nodes for the level
    """

    def __init__(self, input_count, output_count):
        self.inputs = [None for _ in range(input_count)]
        self.outputs = [None for _ in range(output_count)]
        self.biases = [None for _ in range(output_count)]

        # For each input node we have #output_count connections which are our weights
        self.weights = [[None for _ in range(output_count)] for _ in range(input_count)] 
        
        Level.randomize(self)

    def randomize(level):
        """
        Method that randomizes the biases and weights of the given level

        Args:
            level (Level): The level that is going to be randomized
        """

        for i in range(len(level.inputs)):
            for j in range(len(level.outputs)): 
                level.weights[i][j] = random.uniform(-1, 1) # Negative values to help decide which way to turn 
        
        for i in range(len(level.biases)):
            level.biases[i] = random.uniform(-1, 1)

    def feed_forward(given_inputs, level):
        """
        Feeds forward the signal of the input nodes to the output nodes

        Args:
            given_inputs (list) The inputs that are being fed forward in the level
            level (Level): The specific level being used to feed forward the info

        Returns:
            list: A list of the end result with the corresponding output values of the level, used as input values for the next level
        """
         
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