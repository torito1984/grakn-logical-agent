from environment.hoover_environment import Environment
from agent.hoover import HooverAgent
import sched
import time


if __name__ == "__main__":
    # Set the world to turn
    environment = Environment(K=2, N=3, M=3)

    # Set the agent to live in the world
    hoover = HooverAgent(environment, db="localhost:48555", keyspace='wumpus')
    hoover.init()
    hoover.run()
    hoover.close()