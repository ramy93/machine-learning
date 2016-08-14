__author__ = 'ramy93'
import numpy as np
from smartcab.QTable import QTable
from ctypes import *

class Learner:

    def __init__(self, environment, state_dictionary=None, action_dictionary=None, alpha=0.2, gamma=0.9):
        self.environment = environment
        self.state_dictionary = state_dictionary
        self.action_dictionary = action_dictionary
        self.alpha = alpha
        self.gamma = gamma
    #method to be overriden by any learner class
    def update(self, state, action, reward, state_prime):
        print 'Updating environment'
        pass


    # TODO: implement this method correctly
    def get_value(self, state, action):
        actions = {'left': 100, 'right': 2, 'forward': 100, None: 2}
        return actions[action]

    def get_states(self):
        return self.state_dictionary

class QTableLearner(Learner):
    def __init__(self, env, state_dictionary=None, action_dictionary=None, alpha=0.2, gamma=0.8):
        Learner.__init__(self, env, state_dictionary, action_dictionary, alpha, gamma)
        if state_dictionary is None or action_dictionary is None:
            raise Exception("State dictionary and action array cannot be null")

        self.alpha = alpha
        self.gamma = gamma
        self.state_dictionary = state_dictionary
        self.action_array = action_dictionary

        self.num_state_variables = len(state_dictionary)
        self.action_count = len(action_dictionary)

        self.table = QTable(state_dictionary, action_dictionary)

    def get_value(self, state, action):
        action = {'action': action}
        return self.table.get_value(state, action)

    #TODO : verify current implementation
    def update(self, state, action, reward, state_prime):

        currentQ = self.get_value(state, action)
        #print
        #print currentQ, 'Current Q value'
        new_value = (1-self.alpha) * currentQ + self.alpha * (reward + self.gamma * max([ self.get_value(
            state_prime,  action_prime) for action_prime in self.environment.valid_actions ]))

        #print new_value, 'updated Q value'
        self.set_value(state,action,new_value)

        #print self.get_value(state, action)
        #print self.table.table
        return
    def set_value(self, state, action, value):
        action = {'action': action}
        self.table.set_value(state, action, value)

