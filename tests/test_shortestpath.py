from pytest import approx
from warehouseroute.shortestpath import PathFinder


def test_shortest_path(graph1, loc1, loc3):

    # Setup
    po = PathFinder()

    # Get node ID:s
    node1 = graph1.get_node_id_for_location(loc1)
    node3 = graph1.get_node_id_for_location(loc3)

    # Test that shortest_path returns the expected result
    route = po.shortest_path(graph1, node1, node3)
    assert route.cost == approx(2.0)
    assert route.path == [155, 157]

    # Test that shortest_path returns None if there is no path
    route = po.shortest_path(graph1, node3, node1)
    assert route == None
