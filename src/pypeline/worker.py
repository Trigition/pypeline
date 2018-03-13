#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue
from threading import Thread


class Worker(Thread):

    """Workers are assigned to nodes as
    separate threads to execute and solve
    computational problems"""

    def __init__(self, worker_index, start_node, worker_name="Worker"):
        """Initializes a Worker

        :worker_index: TODO
        :worker_name: TODO

        """
        Thread.__init__(self)

        self.worker_index = worker_index
        self.worker_name = worker_name
        self.is_idle = False
        #self.assign_node(start_node)
        start_node.assign_worker(self)
        self.start()

    def assign_node(self, node):
        """Assigns a worker a function to perform
        :node: A node object
        """
        self.cur_node = node

    def run(self):
        """Runs the thread
        """
        self.is_idle = False
        while not self.cur_node.pypeline.is_done():
            try:
                job_input = self.cur_node.get_next_job()
                output = self.cur_node.problem(job_input)
                self.cur_node.output.put(output)
            except queue.Empty:
                # Worker timeout, check to see if node parent's are
                # finished
                if self.cur_node.are_parents_finished():
                    # Parents are finished giving output
                    # this node is now finished processing as well
                    # get a new job
                    self.cur_node.set_done()
                    if self.cur_node.pypeline.assign_worker(self):
                        continue
                    else:
                        break

    def __str__(self):
        """ Overrides the string cast
        of this class
        """
        return '%s-%d' % (self.worker_name, self.worker_index)
