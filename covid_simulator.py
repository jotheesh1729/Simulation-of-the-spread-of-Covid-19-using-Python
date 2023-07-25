from sim_parameters import TRASITION_PROBS, HOLDING_TIMES
import random


class CovidSimulation:
    def __init__(self, id, age_group, country, init_state='H'):
        self.id = id
        self.age_group = age_group
        self.country = country
        self.cur_state = init_state
        self.staying_days = 0
        self.prev_state = init_state

    def simulate(self):
        """
        To run COVID simulation for a single day
        """
        # Check if requires to hold for current state
        if self.isStateHold():
            self.staying_days += 1  # Increase the number of staying days by 1 if stay
        else:
            self.staying_days = 0  # Reset the number of staying days to 0 if no
            self.prev_state = self.cur_state  # Update previous state
            self.cur_state = self.getNextState()  # Get next state/transition

    def getNextState(self):
        """
        To get the next transition based on the given probabilities
        """
        # Get the transition probability dictionary based on its age group and its current state
        prob_dict = TRASITION_PROBS[self.age_group][self.cur_state]

        # Randomly generate a number in a range from 0.01 to 1 (1% - 100%)
        randomVal = float(random.randint(1, 100) / 100)
        offset = 0

        # Based on the randomly generated number, return the selected state
        # Eg. {'H':0.9, 'I':0.1}
        # Value in a range from 0.01 - 0.9 will return 'H'
        # Value in a range from 0.91 - 1.0 will return 'I'
        for state, prob in prob_dict.items():
            if randomVal <= prob + offset:
                return state
            else:
                offset += prob

    def isStateHold(self):
        """
        Check if it needs to hold for current state
        """
        # Get the Holding Time based on its age group and its current state
        expected_holding_days = HOLDING_TIMES[self.age_group][self.cur_state]

        # To Hold if it is larger than 0 and it is still within the number of holding time
        if expected_holding_days != 0:
            if self.staying_days + 1 < expected_holding_days:
                return True
            else:
                return False
        else:  # Not to Hold if it is 0 day
            return False

    def getResults(self):
        """
        Return current state, number of staying days and previous state
        """
        return self.cur_state, self.staying_days, self.prev_state
