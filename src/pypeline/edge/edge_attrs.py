#!/usr/bin/env python
# -*- coding: utf-8 -*-

from queue import Queue

class Edge_Attr():

    """This class holds an edge attributes. Edge attributes
    include problem set buffers, data throughput monitoring, etc"""

    def __init__(self):
        """Initializes edge attributes"""
        self.buffer = Queue()

    def place_data(self, data_dict):
        """Places dict of input parameters for the next stage
        of processing

        :data_dict: A dictionary of input parameters
        """
        self.buffer.put(data_dict)

    def get_data(self):
        """Gets the next data in the buffer
        :returns: A dict of data
        """
        return self.buffer.get()
