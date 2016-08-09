__author__ = 'ramy93'

import random

from environment import Agent, Environment


from planner import RoutePlanner
from simulator import Simulator

#going to inject a learner into
import Learner
from Learner import *

class QLearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, planner=None):
        super(QLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color

        self.planner = planner
        self.simple_planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # TODO: Initialize any additional variables here


    def reset(self, destination=None):
        self.simple_planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.simple_planner.next_waypoint()  # from route planner, also displayed by simulator
        # TODO: Update state
        # TODO: Select action according to your policy

        # TODO: Learn policy based on state, action, reward
        print "Updating Learning agent: "
        self.planner.update()

    def set_planner(self, planner):
        self.planner = planner
