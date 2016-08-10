import numpy as np
class QTable:
    def __init__(self, state_dictionary, action_dictionary):
        self.state_dictionary = state_dictionary
        self.action_dictionary = action_dictionary
        self.num_state_variables = len(state_dictionary)
        self.num_action_variables = len(action_dictionary)

        self.all_states = self.state_dictionary.keys() + self.action_dictionary.keys()
        self.num_all_states = self.num_state_variables + self.num_action_variables


        self.sub_state_reference = np.zeros(range(self.num_all_states))

        index = 0
        for key in self.all_states:
            if key in self.state_dictionary:
                state_values = self.state_dictionary[key]
            else:
                state_values = self.action_dictionary[key]
            self.sub_state_reference[index] = self.SubState(key, state_values)
        '''
        for i in state_dictionary.keys():
            sub_state = self.SubState(i, state_dictionary[i])
            self.state_index[sub_state.get_substate_name()] = index
            self.index_state[index] = sub_state
        '''
        self.QTable = np.zeros([state.get_num_values for state in self.sub_state_reference])

    def get_value(self, state_and_values, action_dictionary):
        if len(state_and_values) + len(action_dictionary) != self.num_all_states:
            raise Exception ("Invalid state requested!")

        location = range(self.num_all_states)
        index = 0

        for sub_state in self.sub_state_reference:
            key = sub_state.get_name()
            if key in state_and_values.keys():
                state_value = state_and_values[key]
            else:
                state_value = action_dictionary[key]
            value = sub_state.get_value_index(state_value)
            location[index]=value
        index += 1
        return self.QTable[tuple(location)]

    class SubState:
        def __init__(self, substate_name, substate_values):
            self.substate_name = substate_name
            self.substate_values = substate_values
            self.values_index = {}

            index = 0
            for i in substate_values:
                self.values_index[i] = index
                index += 1

        def get_num_values(self):
            return len(self.substate_values)

        def get_value_index(self, value):
            return self.values_index[value]

        def get_name(self):
            return self.substate_name