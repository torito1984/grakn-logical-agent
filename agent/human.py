import random
from abc import ABC, abstractmethod
import time
from grakn.client import GraknClient
import string
import numpy as np
from agent.agent import GraknAccesor

class HumanAgent:

    def __init__(self, db, keyspace):
        self.accesor = GraknAccesor(db, keyspace)
        
    def init(self):
        self.accesor.init()
    
    def close(self):
        self.accesor.close()
    
    def randomString(self, stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def insert_order(self, order):
        uuid = self.randomString()
        if order == 'stop':
            query = 'insert $d isa stop'
        else:
            query = 'insert $d isa work'

        self.accesor.insert_sensor(query, 'order-sensor')



  


