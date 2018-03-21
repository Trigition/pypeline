#!/usr/bin/env python
# -*- coding: utf-8 -*-


import networkx as nx

from queue import Queue
from pypeline.node import Node, UtilityNode
from pypeline.worker import Worker


class Pypeline():

    """This class computes a graph
    of dependent problems in the most
    efficient way with multi-threaded
    processing"""

    def __init__(self, num_workers, name='Pypeline', max_timeouts=-1):
        """Initializes a Pypeline """
        if type(num_workers) is not int or num_workers < 1:
            raise ValueError('Only positive integer values allowed')
        if type(max_timeouts) is not int:
            raise ValueError('Only integer values allowed for max timeouts')
        self.num_threads = num_workers
        self.name = name
        self.pype = nx.DiGraph()
        self.max_timeouts = max_timeouts
        self.halt = False
        self.root_nodes = {}
        self.func_node_map = {}
        self.__initialize__graph__()

    def __initialize_workers__(self):
        self.workers = [Worker(i, self.root_nodes['main']) for i in range(self.num_threads)]

    def __initialize__graph__(self, channel_dict={'main':1}):
        """Initializes the graph
        """
        # TODO Have pypeline use channel names
        for channel, nthreads in channel_dict.items():
            #self.root_nodes.append(UtilityNode(self))
            self.root_nodes[channel] = UtilityNode(self)

    def __get_node__(self, func, max_threads=1):
        """Gets the Node containing the passed function.
        If no Node exists, one is created and a map record
        is made
        
        :func: The passed function
        :max_threads: The maximum number of threads for
        a new node. If a node already exists for the function,
        this parameter is ignored.
        :return: A node encapsulating the function
        """
        if func in self.func_node_map:
            return self.func_node_map[func]
        else:
            node = Node(func, self, max_threads=max_threads)
            self.func_node_map[func] = node
            return node

    def link(self, func1, func2=None, func1_max_threads=1, func2_max_threads=1, parent_channel='main'):
        """Links the output of function1 to function2

        :func1: The 'feeding' function
        :func2: The next function which 'feeds'. If input is None,
        then func1 will be used as a direct input node
        :func1_max_threads: The maximum number of threads to be used on
        func1
        :func2_max_threads: The maximum number of threads to be used on
        func2
        :parent_channel: Used if func2 is None. Func1 will be used as a
        destination node for the specified input channel

        """
        # Base case, only func1 is passed
        func_map = self.func_node_map
        if func2 is None:
            # Check to see if func1 is in defined functions
            src_node = self.root_nodes[parent_channel]
            dst_node = self.__get_node__(func1, func1_max_threads)
        else:
            src_node = self.__get_node__(func1, func1_max_threads)
            dst_node = self.__get_node__(func2, func2_max_threads)

        # Finally add edge for pypeline
        self.pype.add_edge(src_node, dst_node)

    def assign_worker(self, worker):
        """Assigns a worker to the next node

        :worker: A reference to the worker being assigned

        """
        # Find nodes which are waiting for input
        for node in self.pype.nodes:
            if node.color == Node.State.waiting:
                node.assign_worker(worker)
                return True
        # No waiting node found, assume pype has finished
        # execution
        return False

    def load_data(self, inputs):
        """Runs the Pypeline on a list of inputs

        :inputs: A list of data for the input nodes to process

        """
        # TODO Find a way for Pypeline to figure out which
        # input goes to which ROOT node
        self.input = Queue()
        if type(inputs) is list:
            [self.input.put(i) for i in inputs]
        else:
            self.input.put(inputs)

    def is_done(self):
        """Checks to see if all nodes are set as 'done'
        :returns: True if all nodes have finished computation

        """
        if self.halt:
            return True
        else:
            return all([n.color == Node.State.done for n in self.pype.nodes()])

    def children_of(self, node_ref):
        """Finds the children nodes of a given parent
        node reference

        :node_ref: A reference to a node within a Pypeline
        instance
        :returns: A list of child nodes

        """
        return self.pype.successors(node_ref)

    def parents_of(self, node_ref):
        """Finds the parent nodes of a given child node

        :node_ref: A reference to a node within a Pypeline
        instance
        :returns: A list of parent nodes

        """
        return self.pype.predecessors(node_ref)

    def run(self):
        """Runs the pypeline, will block until all workers have finished
        :returns: The a dict containing output data

        """
        try:
            self.__initialize_workers__()
            for worker in self.workers:
                worker.join()
            # Look for leaf nodes with no output
            p = self.pype
            for node in self.pype.nodes():
                t = (node.problem.__name__, self.pype.out_degree(node), self.pype.in_degree(node))
                print('%s %d %d' % t)
            leaf_nodes = [n for n in p.nodes() if p.out_degree(n) == 0]
            # TODO better output
            result = {}
            for node in leaf_nodes:
                result[node.problem] = list(node.output.queue)
        except KeyboardInterrupt:
            self.halt = True
            print('Waiting for workers to halt')
            for worker in self.workers:
                worker.join()
            raise KeyboardInterrupt('User halting pypeline')
        return result
