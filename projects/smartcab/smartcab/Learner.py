__author__ = 'ramy93'


class Learner:

    def __init__(self, environment):
        self.environment = environment
        self.Qtable = None

    def update(self, agent):
        print 'Updating environment'
        agent_next_waypoint = agent.get_next_waypoint()
        agent_state = agent.get_state()
        print 'agent state'
        print agent_state



