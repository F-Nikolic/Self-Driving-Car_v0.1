# Self-Driving-Car_v0.1

A little side project to deepen my knowledge of neural networks trying to create a self driving car simulation with no ML library usage.

## Table of Contents
- [Project Description](#projectoverview)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)
- [Problem that occured](#problems)
- [What I would Change](#changes)
- [Possible Future Features](#future)
- [Contact](#contact)

## Project Overview

This projects uses the pygame library in python to create a car driving simulation on an infinite road where the car can move freely and collide with traffic and road borders.

The aim of the project is to build a network from scratch and train a self driving car using feed_forward and a genetic algorithm. The fitness function for the algorithm was the smallest y value of the car (since y increases as it moves down the screen) because we want the car to go as far as possible without colliding with an object. 

Collisions were handled by checking for segment intersections using linear interpolation.

The neural network is also visualized next to the car simulation.

For this project I loosely followed a similar project guide: (https://www.youtube.com/watch?v=Rs_rAxEsAvI). Please check it out.

The guide was written in javaScript and the logic differs a bit because of my usage of pygame and python instead.



## Setup

Please use the Anaconda Prompt instead of the terminal/powershell to avoid package installation problems. 
### Step 1: Clone the Repository
First, navigate to a directory of your choice, e.g.,
```bash
cd Documents/PersonalProjects
```
Then, clone the repo to this directory:
```bash
git clone https://github.com/F-Nikolic/Self-Driving-Car_v0.1.git
```
Navigate to the newly created directory:
```bash
cd Self-Driving-Car_v0.1
```
### Step 2: Open Anaconda Prompt
To avoid any compatibility issues, we recommend to use the anaconda prompt that comes with your installation of Anaconda.

### Step 3: Create a new conda environment
Create a new conda environment "myenv" is the name of your environment which you are free to adjust.
```bash
conda create --name myenv 
```
### Step 4: Activate the conda environment
```bash
conda activate myenv
```
### Step 5: Install dependencies from 'requirements.txt'
Install all required dependencies using pip:
```bash
pip install -r requirements.txt
```

## Usage

**Start here:** While being in the anaconda prompt from before, type: 
```bash
python main.py
```
The game loop starts and a screen showing all the car and road objects, as well as a visualization of the network shows up. 

On top of the road there are buttons to save and delete the current neural network.

By pressing the 'R' key, one can reload the game without having to close and open it again. By reloading, the agents load the current saved neural network model (if there is any) and mutate themselves by a given amount.

Note that currently the network only saves manually by clicking the button since the problem to solve is relatively simple.

## License 
The project is licensed under "MIT" license. See LICENSE.md file for more details.

## Problems that occured

Problems that frequently occured where trying to achieve the scroll effect with the car still being centered on the road and being able to overtake other traffic cars.

Furthermore trying to generate more than 200 instances of agent cars are causing quite a bit of lag and drop in frames since they are updating on every frame by the nature of pygame where it draws everything on every frame.

## What I would Change

If I would be to redo this project at one point, I would set up the whole game screen better and read even further into the pygame library. 

I would especially try to optimize the whole simulation better and find a solution so I could generate a higher number of instances without dropping significantly in frames.

## Possible Future Features

Possible features that can be added are:
- Saving the network automatically
- Automatically generating new agents based on epochs
- Endless generating traffic
- Animating the visualization
- Evaluation of the model

## Contact
For any questions, collaborations or support, you can contact me at: 
- Nikolic Filip: fipsii123@gmail.com



