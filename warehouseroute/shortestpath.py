from heapq import heappush, heappop
from graph import Graph


class Route:
    '''
    Route between two nodes in a graph.

    Attributes
    ----------
    path: list of ints, the node ID:s in the path between the locations
    cost: float, the cost to traverse the path
    '''

    def __init__(self, path, cost):
        self.path = path
        self.cost = cost

    def __str__(self):
        return 'Path: '+' '.join(map(str, self.path))+' Distance: '+str(self.cost)


class PathFinder:
    '''
    Class that holds methods for finding the shortest path.

    Currently, PathFinder only contains the A* algorithm and takes a Graph as
    input, but this could be extended with other path finding algorithms and
    other inputs like grids.
    '''

    def __init__(self):
        pass

    def reverse_path(self, came_from: dict[int, int], start: int, end: int) -> list[int]:
        '''
        Reverse the path in the dictionary of parent nodes.

        The dict came_from holds the previous node in the shortest path from
        the start node to the node in the key. Using the dict, recreate the
        shortest path from start node to end node.

        Parameters
        ----------
        came_from: dict, key: node, value: the previous node in the path
        start: int, the node ID of the start node
        end: int, the node ID of the end node

        Returns
        ----------
        path: list of int, the node ID:s in the path between start and end
        '''
        path = [end]
        current = end
        while current != start:
            path.append(came_from[current])
            current = came_from[current]
        path.reverse()
        return path

    def shortest_path(self, G: Graph, start: int, end: int) -> Route:
        '''
        Calculate the shortest path using the A* algorithm

        The A* algoritm is a breadth first algorithm that is guaranteed to find
        a shortest path, if a path exists, and if an "admissible" heuristic is
        used to estimate the cost from any node to the end node. A heuristic is
        admissible if it never overestimates the cost.

        At every iteration, the node on the search frontier that has the lowest
        priority is selected and its connected nodes are investigated. The
        priority of a node is calculated as a sum of the cost so far and an
        estimated cost from the node to the end node. The estimated cost comes
        from a heuristic, which here is Euclidean distance between the
        positions of the two nodes.  The priorities are stored in a priority
        queue to avoid the need to sort the frontier nodes at every iteration.

        In this implementation of the A* algorithm, there is no mechanism for
        breaking ties if two routes are exactly the same length. When driving a
        forklift in a warehouse, the number of turns has a significant impact
        on the travel time and should be used to break ties.

        Parameters
        ----------
        G: Graph, the graph structure of warehouse locations
        start: int, the start node
        end: int, the end node

        Returns
        ----------
        path: Route, object holding the path and the cost of the path
        '''
        # Priority queue to store priority, node, where priority is a sum of
        # (1) the cost so far from the start to the node and
        # (2) an estimated cost from the node to the end
        open_nodes = [(0, start)]

        # Dict to store the previous node in the path for each opened node
        came_from = {}
        came_from[start] = None

        # Dict to store the cost from the start node to each opened node
        cost_so_far = {}
        cost_so_far[start] = 0.0

        while open_nodes:

            # Get the node on the search frontier with the lowest priority,
            # i.e. lowest estimated cost from start to end
            _, current = heappop(open_nodes)

            if current == end:
                # Found path from start to end
                path = self.reverse_path(came_from, start, end)
                return Route(path, cost_so_far[current])

            for neighbor in G.neighbors(current):
                new_cost = cost_so_far[current] + \
                    G.cost(current, neighbor)
                # Ignore nodes that were already visited unless a lower cost
                # path was found
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    priority = new_cost + G.heuristic(neighbor, end)
                    heappush(open_nodes, [priority, neighbor])

        # Found no path from start to end
        return None
