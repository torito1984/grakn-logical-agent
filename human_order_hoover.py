from environment.hoover_environment import Environment
from agent.human import HumanAgent
import sched
import time
import sys

# Possible orders: stop, work
if __name__ == "__main__":
    # Set the agent to live in the world
    human = HumanAgent(db="localhost:48555", keyspace='wumpus')
    human.init()
    order = sys.argv[1]
    print('Ordering to {}'.format(order))
    
    human.insert_order(order)
    human.close()