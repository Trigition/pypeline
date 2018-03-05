#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx

class Pypeline():

    """This class computes a graph
    of dependent problems in the most
    efficient way with multi-threaded
    processing"""

    def __init__(self, num_workers, name='Pypeline'):
        """Initializes a Pypeline """
        if num_workers < 1 or type(num_workers) is not int:
            raise ValueError('Only positive integer values allowed')
        self.num_threads = num_workers
        self.name = name
        self.pypeline = nx.DiGraph()

    def __initialize_workers__(self):
        self.idle_workers = [Worker(i, self.name) for i in range(self.num_threads)]
        self.busy_workers = []

    def __initialize__graph__(self, instructions):
        """Initializes the graph with the passed instructions

        :instructions: TODO
        :returns: TODO

        """
        pass

    def __create_dependency_graph__(self):
        """This method parses the code flow graph
        and builds a dependency graph. This is for
        quickly finding input edges for nodes
        """
        self.dependencies = DiGraph()
        for edge in self.pypeline.edges():
            self.depencencies.add_path(edge[1], edge[0])

    def link(self, func1, func2, func1_max_threads=1, func2_max_threads=1):
        """Links the output of function1 to function2

        :func1: The 'feeding' function
        :func2: The next function which 'feeds'
        """
        src_node = Node(func, self, max_threads=func1_max_threads)
        dst_ndoe = Node(func, self, max_threads=func2_max_threads)
        self.pypeline.add_edge(src_node, dst_node)

    def add_root_func(self, func, max_threads=1):
        """Adds a root func which generates
        input data

        :func: TODO
        :max_threads: TODO
        :returns: TODO

        """
        node = Node(func, self, max_threads=max_threads)
        self.pype.add_node(node)
        self.root_nodes.append(self.pype[node])

    def assign_worker(self, worker):
        """Assigns a worker to the next node

        :worker: TODO
        :returns: TODO

        """
        # Find nodes which are waiting for input
        for node in self.pype.nodes:
            if node.color == Node.State.waiting:
                node.assign_node(worker)
