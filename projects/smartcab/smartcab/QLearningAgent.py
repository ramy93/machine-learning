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

    def __init__(self, env, learner, planner):
        super(QLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color

        self.planner = planner(self.env, self)
        #self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.learner = learner  # this will be reference to injected learner

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        # TODO: Update state
        self.learner.update(self)
        # TODO: Select action according to your policy
        action = self.next_waypoint

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        print "Updating Learning agent: "
        print "deadline: {}\ninputs: {}\naction : {}\nreward: {}\ntime: {}\n".format(deadline, inputs, action, reward, self.env.t)
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

