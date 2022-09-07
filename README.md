# Warehouse Route code sample

This is a code sample in Python that computes the shortest path between two locations in a warehouse using the A* algorithm [(https://en.wikipedia.org/wiki/A*_search_algorithm)](https://en.wikipedia.org/wiki/A*_search_algorithm). It takes as input a JSON file describing the warehouse layout as a graph structure with locations (nodes) and connections between the locations (edges). Every node has the attributes position and location. The position is a 2D position of the node on the warehouse floor. The location is the identifier of the warehouse location, which depends on the type the location.

A warehouse can be organized into different named areas, e.g. pick area X, inbound area Y, which locations can be organized by. The Warehouse Route package supports three different location types that inherit from the abstract base class Location:
- AreaLocation (area)
- RackLocation (area, rack, horizontal and vertical coordinate)
- DeepStackingLocation (area, horizontal and vertical (depth) coordinate)

Area locations can be identified by the area name only, for example, inbound areas, which are just floor areas next to the inbound gates where incoming goods are put down temporarily before being stored. Locations in storage racks or shelves will be identified by an area, rack, horizontal coordinate and vertical coordinate. Deep stacking is storing of goods in a stack, either horizontal or vertical, where only the last unit can be accessed. An example could be rows of refrigerators stacked agains a wall, where the horizontal coordinate identifies which row along the wall and the vertical coordinate identifies the position in the row/stack.

Here is a diagram showing a very simple warehouse layout, with inbound and outbound gates on opposite ends of the building and the storage racks in the middle.

![Warehouse layout](images/Warehouse.drawio.png?raw=true)

## Example input

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
        ],
        ...
    }

## How to get dependencies

To install the required packages using pip:

    pip install -r requirements.txt

The requirements were generated in an environment running Python 3.10.6.

## How to run

To run the simple GUI:

    python warehouseroute/simplegui.py examples/warehouse_with_crossaisle.json

There are two drop-down menus that allow the user to select the start and end location. When the user selects a start or end location, it is highlighted in the warehouse map. When the user presses the "Get route" button, the shortest path is drawn in the map and the distance is displayed.

![Warehouse Route GUI window](images/WarehouseRouteGUI.png?raw=true)

## How to run tests

To run the tests:

    pytest tests
