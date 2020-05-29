import random
import time
from grakn.client import GraknClient
import string
import numpy as np
from agent.agent import Agent, GraknAccesor

class HooverAgent(Agent):

    def __init__(self, enviroment, db, keyspace):
        self.enviroment = enviroment
        self.accesor = GraknAccesor(db, keyspace)
        self.action_weights = {'brush-hoover': 10, 'wheel-advance': 5, 'wheel-rotate-left': 1, 'wheel-rotate-right': 1}

    def init(self):
        self.accesor.init()
    
    def close(self):
        self.accesor.close()

    def insert_position(self, x, y):
        query = 'insert $l isa location-value, has x {}, has y {}'.format(x, y)
        self.accesor.insert_sensor(query, 'location-sensor')
    
    def insert_dirt(self, is_clean, x, y):
        if is_clean:
            query = 'insert $d isa clean, has x {}, has y {}'.format(x, y)
        else:
            query = 'insert $d isa dirty, has x {}, has y {}'.format(x, y)

        self.accesor.insert_sensor(query, 'dirt-sensor')

    def insert_clear(self, advance):
        if advance:
            query = 'insert $d isa can-advance'
        else:
            query = 'insert $d isa blocked'

        self.accesor.insert_sensor(query, 'bump-sensor')
      
    def insert_obsevables(self):
        (x, y) = self.enviroment.get_position()
        clean = self.enviroment.is_clean(x, y)
        advance = self.enviroment.can_advance()
        
        # Insert current position and clean or dirty
        self.insert_position(x, y)
        self.insert_dirt(clean, x, y)
        self.insert_clear(advance)

        print("Finished {}".format(self.enviroment.finished()))
        print(self.enviroment.state())

    def execute_action(self, action):
        if action[0] == 'brush-hoover':
            self.enviroment.clean()
        elif action[0] == 'wheel-rotate-left':
            self.enviroment.rotate_left()
        elif action[0] == 'wheel-rotate-right':
            self.enviroment.rotate_right()
        elif action[0] == 'wheel-advance':
            self.enviroment.advance()
        else:
            print("Action not recognised {}".format(action))


    def actions_to_do(self):
        return self.accesor.read_actions()

    # What happens if more than 1 action is possible?
    def choose_action(self, actions):
        # Take at random if more than 1 option
        weights = np.array([self.action_weights[action[0]] for action in actions])
        weights = weights/weights.sum()
        return actions[np.random.choice(len(actions), 1, p=weights)[0]]




  


