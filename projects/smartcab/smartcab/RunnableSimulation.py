__author__ = 'ramy93'

from agent import LearningAgent
from simulator import Simulator
from environment import Environment
import QLearningAgent

class RunnableSimulation:

    def __init__(self, update_delay=0.5, display=True, n_trials=100):
        self.display = display
        self.update_delay = update_delay
        self.n_trials = n_trials

    def run(self, environment):
        """Run the agent for a finite number of trials."""
        sim = Simulator(environment, None, self.update_delay, self.display)  # create simulator (uses pygame when display=True, if available)
        # NOTE: To speed up simulation, reduce update_delay and/or set display=False

        sim.run(self.n_trials)  # run for a specified number of trials
        # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    env = Environment()
    a = env.create_agent(LearningAgent)
    env.set_primary_agent(a, enforce_deadline=True)
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    simulation = RunnableSimulation(env)
    simulation.run()



