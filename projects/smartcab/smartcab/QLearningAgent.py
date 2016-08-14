__author__ = 'ramy93'

from environment import Agent
from planner import RoutePlanner

class QLearningAgent(Agent):

    def __init__(self, env, planner=None):
        super(QLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color

        self.planner = planner
        self.simple_planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

    def reset(self, destination=None):
        self.simple_planner.route_to(destination)
        self.planner.route_to(destination)

    def update(self, t):
        self.next_waypoint = self.simple_planner.next_waypoint()  # from route planner, also displayed by simulator
        self.planner.update()

    def set_planner(self, planner):
        self.planner = planner
