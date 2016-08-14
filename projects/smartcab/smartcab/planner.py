import random
import numpy as np

class Planner:
    def __init__(self, env, agent, planner_statistics=None):
        self.env = env
        self.agent = agent
        self.destination = None
        self.planner_statistics = planner_statistics
    # method to be overriden by all subclasses
    def next_waypoint(self):
        pass

    # method to be overriden by intelligent planners
    def update(self):
        pass

    def route_to(self, destination=None):
        self.destination = destination if destination is not None else random.choice(self.env.intersections.keys())

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
        self.planning_heuristics = {}
        self.temperature = 1000
    def set_learner(self, learner):
        self.learner = learner

    def update(self):

        old_state = {}
        old_inputs = self.env.sense(self.agent)
        for key in self.learner.get_states():
            if key in old_inputs:
                old_state[key] = old_inputs[key]
            elif key in self.env.agent_states[self.agent]:
                old_state[key] = self.env.agent_states[self.agent][key]
            elif key in self.planning_heuristics:
                old_state[key] = self.get_heuristic_value(self.planning_heuristics[key])

        action = self.get_next_waypoint(old_state, self.env.valid_actions)
        reward = self.env.act(self.agent, action)
        inputs = self.env.sense(self.agent)
        state = {}
        for key in self.learner.get_states():
            if key in inputs:
                state[key] = inputs[key]
            elif key in self.env.agent_states[self.agent]:
                state[key] = self.env.agent_states[self.agent][key]
            elif key in self.planning_heuristics:
                state[key] = self.get_heuristic_value(self.planning_heuristics[key])
        self.learner.update(old_state, action, reward, state)
        if self.planner_statistics is not None:
            self.planner_statistics.update(self.agent)

        return

    def next_waypoint(self):
        return self.get_next_waypoint(self.agent.get_state(), self.env.valid_actions)
        #return random.choice(self.env.valid_actions)

    def get_next_waypoint(self, state, actions):
        deadline = self.env.get_deadline(self.agent)
        if deadline is None:
            temperature_subtraction = 30 * self.env.t
            if temperature_subtraction < 500 :
                temperature = 500 - temperature_subtraction
            else:
                temperature = 0.1
        else:
            self.temperature = max(self.temperature*0.99, 0.1)
        values = np.array([np.exp(self.learner.get_value(state, action)/self.temperature) for action in actions])
        values = values / np.sum(values)
        index = np.where(np.random.multinomial(1, values))[0][0]
        return actions[index]

    def add_heuristic(self,  heuristic_name, method):
        heuristic = self.Heuristic(heuristic_name, method)
        self.planning_heuristics[heuristic.get_name()] = heuristic

    def get_heuristic_value(self, heuristic):
        return heuristic.get_value()

    def set_planner_statistics(self, planner_statistics_implementation):
        self.planner_statistics = planner_statistics_implementation

    class Heuristic:
        def __init__(self, heuristic_name, method):
            self.heuristic_name = heuristic_name
            self.heuristic_method = method

        def get_value(self):
            return self.heuristic_method.get_value()

        def get_name(self):
            return self.heuristic_name


class planner_statistics:
    def __init__(self, weighted=False):
        self.results = []
        self.weighted = weighted
    def update(self, agent):
        agent_state = agent.get_state()
        if agent_state['destination'][0] == agent_state['location'][0] and agent_state['destination'][1] == agent_state['location'][1]:
            if not self.weighted:
                self.results.append(1)
            else:
                self.results.append(max(1*agent.get_state()['deadline'],1))
            return
        if agent.get_state()['deadline']<=0:
            self.results.append(0)
            return
        return

    def get_results(self):
        return self.results

# method abstract class
class Method:
    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment

    def get_value(self):
        raise NotImplementedError("method not implemented for interface")


class is_correct_y_direction(Method):  # true, false method
    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment

    def get_value(self):
        state = self.agent.get_state()
        location = state['location']
        destination = state['destination']
        heading = state['heading']
        y_diff = destination[1] - location[1]

        if y_diff >0 and heading[1]>0:
            return True
        elif y_diff < 0 and heading[1] <0:
            return True
        elif y_diff >0 and heading[1] <=0:
            return False
        elif y_diff < 0 and heading[1] >= 0:
            return False
        return True


class is_correct_x_diretion(Method):
    #true, false method
    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment
    def get_value(self):
        state = self.agent.get_state()
        location = state['location']
        destination = state['destination']
        heading = state['heading']
        x_diff = destination[0] - location[0]


        if x_diff >0 and heading[0]>0:
            return True
        elif x_diff < 0 and heading[0] <0:
            return True
        elif x_diff >0 and heading[0] <=0:
            return False
        elif x_diff < 0 and heading[0] >= 0:
            return False
        return True


class agent_traffic_light(Method):
    # [red, green] method
    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment

    def get_value(self):
        state = self.environment.sense(self.agent)
        traffic_light = state['light']
        return traffic_light


class simple_planner_output(Method):
    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment

    def get_value(self):
        return self.agent.next_waypoint


class agent_oncoming(Method):
    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment

    def get_value(self):
        return self.environment.sense(self.agent)['oncoming']


class agent_left_check(Method):
    def __init__(self, agent, environment):
        Method.__init__(self, agent, environment)

    def get_value(self):
        return self.environment.sense(self.agent)['left']


class agent_right_check(Method):
    def __init__(self, agent, environment):
        Method.__init__(self, agent, environment)

    def get_value(self):
        return self.environment.sense(self.agent)['right']
