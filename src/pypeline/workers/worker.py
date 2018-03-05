#!/usr/bin/env python
# -*- coding: utf-8 -*-

from queue import Queue

class Worker(Thread):

    """Workers are assigned to nodes as
    separate threads to execute and solve
    computational problems"""

    def __init__(self, worker_index, worker_name="Worker"):
        """Initializes a Worker

        :worker_index: TODO
        :worker_name: TODO

        """
        Thread.__init__(self)

        self.worker_index = worker_index
        self.worker_name = worker_name
        self.is_idle = False

    def assign_node(self, node):
        """Assigns a worker a function to perform
        :node: A node object
        """
        self.cur_node = node

    def run(self):
        """Runs the thread
        """
        self.is_idle = False
        while True:
            try:
                job_input = self.cur_node.get_next_job()
                output = self.cur_node.problem(**job_input)
            except queue.Empty():
                # Worker timeout, check to see if node parent's are
                # finished
                if self.cur_node.are_parents_finished():
                    # Parents are finished giving output
                    # this node is now finished processing as well
                    self._is_idle = True
                    self.cur_node.set_done()
                    break
                else:
                    # TODO Contact Pypeline to see which node needs
                    # computation
                    continue
        # Currently results in another callstack, find a way for 
        # pypeline instance to allocate workers itself async
        if self.cur_node.pypeline is not None:
            self.cur_node.pypeline.assign_worker(self)
    
    def __str__(self):
        """ Overrides the string cast
        of this class
        """
        return '%s-%d' % (self.worker_name, self.worker_index)
