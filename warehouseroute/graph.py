from enum import Enum
from math import sqrt
# import itertools
from location import Location


class NodeType(Enum):
    RACK = 1
    AREA = 2
    DEEPSTACKING = 3


class Position:
    '''
    Class that represents a 2D position.

    Attributes
    ----------
    x, float: x coordinate
    y, float: y coordinate
    '''

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x ' + str(self.x) + ' y ' + str(self.y)


class Edge:
    '''
    Class that represents an edge in a graph.

    Attributes
    ----------
    to_node: int, to-node ID
    cost: float, the cost to traverse to the to-node
    '''

    def __init__(self, to_node: int, cost: float):
        self.to_node = to_node
        self.cost = cost

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.to_node == other.to_node
        else:
            return False


class Node:
    '''
    Class that represents a node in a graph.

    Attributes
    ----------
    id: int, the node ID
    location: Location, the name of the location
    position: Position, a point
    edges: list of Edges, connections to other nodes
    '''

    def __init__(self, id: int, location: Location, position: Position):
        self.id = id
        self.location = location
        self.position = position
        self.edges = []

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id and \
                self.location == other.location
        else:
            return False

    def __str__(self):
        return 'node ' + str(self.id)

    def add_edge(self, node_to: int, cost: float):
        '''
        Add an edge to the node
        
        Parameters
        ----------
        node_to: int
        cost: float
        '''
        edge = Edge(node_to, cost)
        if edge not in self.edges:
            self.edges.append(edge)


class Graph:
    '''
    Class that represents a graph structure of nodes and edges.

    Attributes:
    ----------
    nodes: list[Node], the nodes in the graph
    '''

    def __init__(self):
        self.nodes = {}

    def __str__(self):
        return 'nodes ' + str(len(self.nodes))

    def add_node(self, node: Node):
        ''' Add a node to the graph '''
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def len(self):
        ''' Get the number of nodes in the graph '''
        return len(self.nodes)

    def neighbors(self, nodeid: int) -> list[int]:
        '''
        Get the nodes connected to the input node.

        Parameters
        ----------
        nodeid: int, node ID

        Returns
        ----------
        neighbor_ids: list of node ID:s of neighboring nodes
        '''
        node = self.nodes[nodeid]
        edges = node.edges
        neighbor_ids = [e.to_node for e in edges]
        return neighbor_ids

    def cost(self, node_from: int, node_to: int) -> float:
        '''
        Get the cost of the edge from node_from to node_to.

        Parameters
        ----------
        node_from: int, node ID
        node_to: int, node ID

        Returns
        ----------
        cost: float, cost of the edge
        '''
        cost = None
        node_from_edges = self.nodes[node_from].edges
        for edge in node_from_edges:
            if edge.to_node == node_to:
                cost = edge.cost
                break
        return cost

    def get_node_for_location(self, location: Location) -> Node:
        '''
        Get the graph node corresponding to the input location name.

        Parameters
        ----------
        location: Location, the location object

        Returns
        ----------
        node: Node, graph node
        '''
        matching_nodes = []
        for id, node in self.nodes.items():
            if node.location == location:
                matching_nodes.append(node)

        if len(matching_nodes) == 1:
            return matching_nodes[0]
        elif len(matching_nodes) == 0:
            raise ValueError('No node for location '+str(location))
        else:
            raise ValueError('More than one nodes for location '+str(location))

    def get_node_id_for_location(self, location: Location) -> int:
        '''
        Get the graph node ID corresponding to the input location name.

        Parameters
        ----------
        location: Location

        Returns
        ----------
        nodeid: int, graph node ID
        '''
        node = self.get_node_for_location(location)
        return node.id

    def heuristic(self, node1: int, node2: int) -> float:
        '''
        Heuristic used in the A* algorithm to estimate the distance from node
        1 to node 2 using Euclidean distance.

        Parameters
        ----------
        node1: int, start node
        node2: int, end node

        Returns
        ----------
        dist: float, Manhattan distance between the positions of the nodes
        '''
        a: Position = self.nodes[node1].position
        b: Position = self.nodes[node2].position
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return sqrt(dx * dx + dy * dy)

    def get_locations(self) -> list[Location]:
        ''' Get list of the locations in the graph '''
        locations = [n.location for n in self.nodes.values()]
        return locations
