import json
from graph import Edge, Graph, Node, NodeType, Position
from location import Location, AreaLocation, RackLocation, DeepStackingLocation


class GraphParser:
    '''
    Parser for Graph objects

    This is a parser for reading a graph of warehouse locations from a JSON
    file into a Graph object. The JSON should contain a list of nodes, with
    attributes that give the node ID, the position of the node, the warehouse
    location it corresponds to, and its adjacencies or connected nodes. Here is
    an example of the JSON structure:

        {
            nodes:
            [
                {
                    "id": 0,
                    "position": {
                        "x": 12.5,
                        "y": 28.5
                    },
                    "location": {
                        "locationType": 1,
                        "mha": "PICK2",
                        "rack": "5",
                        "horcoor": "10",
                        "vercoor": "10"
                    },
                    "adjacencies": [
                        {
                            "nodeTo": 1,
                            "cost": 0.73
                        }
                    ]
                }
            ]
        }
    '''

    def __init__(self):
        pass

    def __parse_location(self, locationobj: object) -> Location:
        ''' Parse a location object based on its type '''
        node_type = NodeType(locationobj['locationType'])
        mha = locationobj['mha']
        if node_type == NodeType.AREA:
            location = AreaLocation(mha)
        elif node_type == NodeType.RACK:
            rack = str(locationobj['rack'])
            horcoor = str(locationobj['horcoor'])
            vercoor = str(locationobj['vercoor'])
            location = RackLocation(mha, rack, horcoor, vercoor)
        elif node_type == NodeType.DEEPSTACKING:
            horcoor = str(locationobj['horcoor'])
            vercoor = str(locationobj['vercoor'])
            location = DeepStackingLocation(mha, horcoor, vercoor)
        else:
            raise ValueError('Invalid node location type')
        return location

    def __parse_edge(self, nodeid: int, edgeobj: object) -> Edge:
        ''' Parse an edge object '''
        node_to = edgeobj['nodeTo']
        distance = edgeobj['cost']
        return (node_to, distance)

    def __parse_node(self, nodeobj: object) -> Node:
        ''' Parse a node object '''
        nodeid = nodeobj['id']
        xpos = nodeobj['position']['x']
        ypos = nodeobj['position']['y']
        position = Position(xpos, ypos)
        location = self.__parse_location(nodeobj['location'])
        node = Node(nodeid, location, position)
        for edgeobj in nodeobj['adjacencies']:
            node_to, cost = self.__parse_edge(nodeid, edgeobj)
            node.add_edge(node_to, cost)
        return node

    def parse_json(self, filename: str) -> Graph:
        '''
        Return graph object from graph JSON file

        Parameters
        ----------
        filename: str, name of JSON file

        Returns
        ----------
        G: Graph object

        Example
        ----------
        {
            nodes:
            [
                {
                    "id": 0,
                    "position": {
                        "x": 12.5,
                        "y": 28.5
                    },
                    "location": {
                        "locationType": 1,
                        "mha": "PICK2",
                        "rack": "5",
                        "horcoor": "10",
                        "vercoor": "10"
                    },
                    "adjacencies": [
                        {
                            "nodeTo": 1,
                            "cost": 0.73
                        }
                    ]
                }
            ]
        }
        '''
        G = Graph()
        with open(filename) as gfile:
            node_list = json.load(gfile)
            for nodeobj in node_list:
                node: Node = self.__parse_node(nodeobj)
                G.add_node(node)
        return G
