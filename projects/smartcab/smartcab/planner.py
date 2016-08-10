import random
import numpy as np

class Planner:
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.destination = None

    # method to be overriden by all subclasses
    def next_waypoint(self):
        pass

    # method to be overriden by intelligent planners
    def update(self):
        pass

    def route_to(self, destination=None):
        self.destination = destination if destination is not None else random.choice(self.env.intersections.keys())
        print "RoutePlanner.route_to(): destination = {}".format(destination)  # [debug]

class RoutePlanner(Planner):
    """Silly route planner that is meant for a perpendicular grid network."""


    def next_waypoint(self):
        location = self.env.agent_states[self.agent]['location']
        heading = self.env.agent_states[self.agent]['heading']
        delta = (self.destination[0] - location[0], self.destination[1] - location[1])
        if delta[0] == 0 and delta[1] == 0:
            return None
        elif delta[0] != 0:  # EW difference
            if delta[0] * heading[0] > 0:  # facing correct EW direction
                return 'forward'
            elif delta[0] * heading[0] < 0:  # facing opposite EW direction
                return 'right'  # long U-turn
            elif delta[0] * heading[1] > 0:
                return 'left'
            else:
                return 'right'
        elif delta[1] != 0:  # NS difference (turn logic is slightly different)
            if delta[1] * heading[1] > 0:  # facing correct NS direction
                return 'forward'
            elif delta[1] * heading[1] < 0:  # facing opposite NS direction
                return 'right'  # long U-turn
            elif delta[1] * heading[0] > 0:
                return 'right'
            else:
                return 'left'


class IntelligentPlanner(Planner):

    def __init__(self, env, agent, learner=None):
        Planner.__init__(self, env, agent)
        self.learner = learner

    def set_learner(self, learner):
        self.learner = learner

    def update(self):
        action = self.next_waypoint()
        reward = self.env.act(self.agent, action)
        deadline = self.env.get_deadline(self.agent)

        inputs = self.env.sense(self.agent)
        state = self.env.agent_states[self.agent]
        print "deadline: {}\ninputs: {}\naction : {}\nreward: {}\ntime: {}\nstate: {}".format(deadline, inputs, action,
                                                                                              reward, self.env.t, state)
        pass

    # TODO: implement intelligent get_next_move
    def next_waypoint(self):
        return self.get_next_waypoint(self.agent.get_state(), self.env.valid_actions)
        #return random.choice(self.env.valid_actions)

    def get_next_waypoint(self, state, actions):
        deadline = self.env.get_deadline(self.agent)
        if deadline is None:
            temperature_subtraction = 30 * self.env.t
            if temperature_subtraction > 500 :
                temperature = 500 - self.env.t
            else:
                temperature = 0.1
        else:
            temperature = 400 * (self.env.get_deadline(self.agent)) + 1

        values = np.array([np.exp(self.learner.get_value(state, action)/temperature) for action in actions])
        values = values / np.sum(values)
        print values
        index = np.where(np.random.multinomial(1, values))[0][0]
        return actions[index]

