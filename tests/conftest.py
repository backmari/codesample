from pytest import fixture
from warehouseroute.graph import Graph, Node, Position
from warehouseroute.location import AreaLocation, RackLocation


@fixture
def loc1():
    return RackLocation("BUFF2", "15", "20", "1")


@fixture
def node1(loc1):
    pos = Position(62.0, 37.4)
    return Node(155, loc1, pos)


@fixture
def node2():
    pos = Position(19.3, 4.0)
    loc = RackLocation("BUFF2", "12", "34", "1")
    return Node(156, loc, pos)


@fixture
def loc3():
    return AreaLocation("BUFF4")


@fixture
def node3(loc3):
    pos = Position(19.3, 4.0)
    return Node(157, loc3, pos)


@fixture
def graph1(node1, node2, node3):
    graph = Graph()
    node1.add_edge(node2.id, 1.0)
    node1.add_edge(node3.id, 2.0)
    node2.add_edge(node3.id, 3.0)
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    return graph
