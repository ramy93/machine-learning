__author__ = 'ramy93'

from environment import Environment

from agent import LearningAgent
from planner import RoutePlanner
from simulator import Simulator
import QLearningAgent

class RunnableSimulation:

    def __init__(self):
        pass

    def run(self):
        """Run the agent for a finite number of trials."""
        # Set up environment and agent
        e = Environment()  # create environment (also adds some dummy traffic)
        a = e.create_agent(LearningAgent)  # create agent
        e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
        # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

        # Now simulate it
        sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
        # NOTE: To speed up simulation, reduce update_delay and/or set display=False

        sim.run(n_trials=100)  # run for a specified number of trials
        # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    simulation = RunnableSimulation()
    simulation.run()



