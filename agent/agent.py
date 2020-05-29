from abc import ABC, abstractmethod
import random
import time
from grakn.client import GraknClient
import string
import numpy as np

class Agent(ABC):
   
    def __init__(self):
        pass

    @abstractmethod
    def insert_obsevables(self):
        pass

    @abstractmethod
    def actions_to_do(self):
        pass
    
    @abstractmethod
    def choose_action(self, actions):
        pass

    @abstractmethod
    def execute_action(self, action):
        pass

    def run(self):
        while True:
            # Sense the world
            self.insert_obsevables()

            print('Deciding action..')
            actions = self.actions_to_do()

            if actions is None: # If we did not find anything to do, wait for a second
                print("Sleeping")
                time.sleep(0.1)
            elif len(actions) == 1:
                self.execute_action(actions[0])
            else:
                self.execute_action(self.choose_action(actions))


class GraknAccesor:
   
    def __init__(self, db, keyspace):
        self.db = db
        self.keyspace = keyspace
    
    def init(self):
        self.session = GraknClient(uri=self.db).session(keyspace=self.keyspace)

    def close(self):
        self.session.close()

    def insert(self, queries):
       with self.session.transaction().write() as  transaction:
            for i, query in enumerate(queries):
                #print(query)
                #print("- - - - - - - - - - - - - -")
                transaction.query(query)
            transaction.commit()

    def randomString(self, stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def insert_sensor(self, query, sensor_name):
        uuid = self.randomString()
        query = query + ', has uuid "{}";'.format(uuid)
        queries = [query] + self.update_sensor(sensor_name, uuid)
        self.insert(queries)

    def read_actions(self):
        with self.session.transaction().read() as transaction:
            action_list = list(transaction.query('match $d (what: $w, on: $o) isa do; get;'))

            if len(action_list) == 0:
                return None
            else:
                return [(i.map()['w'].type().label(), i.map()['o'].type().label()) for i in action_list]

    def get_session(self):
        return self.session

    def update_sensor(self, sensor_name, uuid):
        create= """match
        $d isa {};
        $n isa no-val;
        $current (input: $d, observed: $o, next: $n) isa sense;
        $ds isa observable, has uuid "{}";
        insert (input: $d, prev : $o, observed: $ds, next: $n) isa sense;""".format(sensor_name, uuid)

        ## update previous observation
        link = """match
        $d isa {};
        $ds isa observable, has uuid "{}";
        $current (observed: $ds, prev: $p) isa sense;
        $old_previous (prev : $pp, observed: $p) isa sense;
        insert (input: $d, prev : $pp, observed: $p, next: $ds) isa sense;""".format(sensor_name, uuid)

        delete = """match
        $d isa {};
        $ds isa observable, has uuid "{}";
        $n isa no-val;
        $current (observed: $ds, prev: $p) isa sense;
        $old_previous (input: $d, prev: $pp, observed: $p, next: $n) isa sense;
        delete $old_previous;""".format(sensor_name, uuid)

        return [create, link, delete]
