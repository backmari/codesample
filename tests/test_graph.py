from pytest import approx
from warehouseroute.graph import Graph, Node, Position
from warehouseroute.location import AreaLocation, RackLocation


def test_add_edge_to_node(node1):

    assert len(node1.edges) == 0

    # Add one edge to the node - number of edges should increase to 1
    node1.add_edge(5, 4.2)
    assert len(node1.edges) == 1

    # Add already existing edge - number of edges should still be 1
    node1.add_edge(5, 4.2)
    assert len(node1.edges) == 1

    # Add a different edge to the node - number of edges should increase to 2
    node1.add_edge(8, 2.0)
    assert len(node1.edges) == 2


def test_add_node_to_graph(node1, node2):

    # Create new graph object
    graph = Graph()
    assert graph.len() == 0

    # Add one node to the graph - number of nodes should increase to 1
    graph.add_node(node1)
    assert graph.len() == 1

    # Add already existing node to the graph - number of nodes should still be 1
    graph.add_node(node1)
    assert graph.len() == 1

    # Add another node to the graph - number of nodes should increase to 2
    graph.add_node(node2)
    assert graph.len() == 2


def test_graph_node_neighbors(graph1, node1, node2, node3):

    # Test that the neighbors method returns the expected neighbors
    node1_neighbors = graph1.neighbors(node1.id)
    assert node2.id in node1_neighbors
    assert node3.id in node1_neighbors
    assert len(node1_neighbors) == 2

    # Test that the neighbors method returns no neighbors if there are none
    node3_neighbors = graph1.neighbors(node3.id)
    assert len(node3_neighbors) == 0


def test_graph_edge_cost(graph1, node1, node2):

    # Test that the cost method returns the correct cost
    cost12 = graph1.cost(node1.id, node2.id)
    assert cost12 == approx(1.0)

    # Test that the cost method returns None if the edge is not in the graph
    cost21 = graph1.cost(node2.id, node1.id)
    assert cost21 == None


def test_get_node_id_for_location(loc1, node1, loc3, node3, graph1):

    # Test that method returns the correct node for a RackLocation
    nodeid1 = graph1.get_node_id_for_location(loc1)
    assert nodeid1 == node1.id

    # Test that method returns the correct node for an AreaLocation
    nodeid3 = graph1.get_node_id_for_location(loc3)
    assert nodeid3 == node3.id
