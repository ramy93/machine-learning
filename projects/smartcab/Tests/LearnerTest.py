from smartcab import QLearningAgent
from smartcab.environment import Environment
from smartcab.Learner import *
from smartcab.agent import *

def main():
    environment = Environment()
    agent = environment.create_agent(LearningAgent)
    environment.set_primary_agent(agent)
    learner = Learner(environment, agent)




if __name__ == "__main__":
    main()