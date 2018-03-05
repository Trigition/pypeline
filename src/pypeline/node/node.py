#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class Node():

    class State(Enum):
        """Represents a Node's state"""
        unvisited = 1
        running = 2
        waiting = 3
        done = 4

    """This class holds a single computational problem
    (specified by the user). The problem's interior computation
    must not be dependent on any other input. If the
    computation is dependent then those dependencies must be
    handled by the node's parent(s)"""

    def __init__(self, func, pypeline, max_threads=1):
        """Initializes a node with a function and it's
        accepted input parameters
        :func: The atomic function for this node to compute
        """
        self.problem = func
        self.max_threads = max_threads
        self.output = Queue()
        self.color = State.unvisited
        self.pypeline = pypeline

    def get_next_job(self):
        """Breaks off data from any of the input jobs
        Currently behavior prioritizes largest queue to pull
        from first
        :returns: Data from the largest input queue
        TODO Implement some form of priority for bottleneck nodes
        """
        parent_nodes = self.pypeline.predecessors(self)
        priority_queue = Node.get_largest_queue(parent_nodes)
        job = priority_queue.get(timeout=1)
        return job

    def assign_worker(self, worker_ref):
        """Assigns a new free worker to the Node
        :worker_ref: A reference to the worker being assigned
        """
        # Assigns a worker to a node
        worker_ref.assign_node(self) # Use double dispatch
        worker_ref.run()
        self.color = State.running
        # Set children nodes to be waiting
        children = self.pypeline.ancestors(self)
        for child in children:
            child.color = State.waiting

    def are_parents_finished(self):
        """ This method checks to see if parent's
        are done sending input parameters
        :returns: True if parent's are all done
        """
        parent_nodes = self.pypeline.predecessors(self)
        parents_done = [p.color == State.done for p in parent_nodes]
        if all(parents_done):
            return True
        else:
            return False

    def set_done(self):
        """Sets the node status to be finished
        """
        self.color = State.done

    @staticmethod
    def get_largest_queue(nodes):
        """Returns the largest of a list of queues
        :queues: A list of input nodes
        :returns: A reference to the largest queue
        """
        queues = [n.output for n in nodes]
        largest_len, largest_queue = (len(queues[0]), queues[0])
        for q in queues[1:]:
            if len(q) > largest_len:
                largest_len = len(q)
                largest_queue = q

        return largest_queue
