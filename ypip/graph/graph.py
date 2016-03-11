# MIT License
# Copyright (c) 2016 Genome Research Limited
from typing import List, Optional, Union


class NodeExists(Exception):
    pass

class NodeDoesNotExist(Exception):
    pass


class Node(object):
    def __init__(self, graph:'DirectedGraph', identity:str, payload:Optional[object] = None):
        self._graph = graph
        self.identity = identity
        self.payload = payload

    def link_to(self, *nodes:Union[str, 'Node']):
        for node in nodes:
            try:
                identity = node.identity
            except AttributeError:
                identity = node

            if identity in self._graph:
                _, links = self._graph[self.identity]
                links.add(identity)

            else:
                raise NodeDoesNotExist('Cannot link <{}> to <{}> as it doesn\'t exist'.format(self.identity, identity))


class DirectedGraph(object):
    def __init__(self):
        self._graph = {}

    def add_node(self, identity:str, payload:Optional[object] = None) -> Node:
        if identity not in self._graph:
            new_node = Node(self._graph, identity, payload)
            self._graph[identity] = new_node, set()
            return new_node

        else:
            raise NodeExists('<{}> already exists'.format(identity))

    def get_node(self, identity:str) -> Node:
        if identity in self._graph:
            node, _ = self._graph[identity]
            return node

        else:
            raise NodeDoesNotExist('No such node <{}>'.format(identity))
