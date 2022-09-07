import argparse
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from parser import GraphParser
from shortestpath import PathFinder


class WarehouseRouteGUI():
    '''
    Warehouse Route GUI

    Simple GUI to display the functionality of the Warehouse Route package.
    Draws the graph based on the node positions and lets the user select the
    start and end location of the route based on the location names associated
    with the nodes. When the user pushes the button 'Get route', the A*
    algorithm is used to find the shortest route. The route is highlighted in
    the warehouse map and the cost/distance is displayed above the map.

    The warehouse graph JSON file is provided as a command line argument. 
    '''

    def __init__(self, root):

        # Parse arguments
        arg_parser = argparse.ArgumentParser(
            description='Get shortest distance between two warehouse locations and plot the route.')
        arg_parser.add_argument('graphfile', type=str, help='graph JSON file')
        args = arg_parser.parse_args()

        # Parse graph file
        graph_parser = GraphParser()
        self.G = graph_parser.parse_json(args.graphfile)
        self.nodedict = self.G.nodes

        # Add main frame that other components are added to
        mainframe = ttk.Frame(root)

        # Create dict with
        # key: Location as string
        # value: Location object
        # since the location dropbox values must be strings
        locations = self.G.get_locations()
        self.locationdict = {}
        for loc in locations:
            self.locationdict[str(loc)] = loc

        # Start location drop-down list
        self.start_combobox = ttk.Combobox(mainframe)
        self.start_combobox.bind("<<ComboboxSelected>>", self.draw_startloc)
        self.start_combobox['values'] = locations
        self.start_combobox.current(0)

        # End location drop-down list
        self.end_combobox = ttk.Combobox(mainframe)
        self.end_combobox.bind("<<ComboboxSelected>>", self.draw_endloc)
        self.end_combobox['values'] = locations
        self.end_combobox.current(0)

        # Button to trigger shortest path calculation
        button = ttk.Button(mainframe, text="Get route",
                            command=self.get_route)

        # Text label for displaying the route distance
        distlabel = ttk.Label(mainframe, text="Distance:")
        self.distvar = StringVar()
        distvalue = ttk.Label(mainframe, textvariable=self.distvar)

        # Figure for drawing the graph and shortest route
        fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=mainframe)

        # Draw all locations and connections
        self.draw_graph()

        # Place components in the main frame
        mainframe.grid(column=0, row=0)
        self.start_combobox.grid(column=0, row=0)
        self.end_combobox.grid(column=1, row=0)
        button.grid(column=2, row=0)
        distlabel.grid(column=0, row=1)
        distvalue.grid(column=1, row=1)
        self.canvas.get_tk_widget().grid(column=0, row=2, columnspan=3)

        # Setup for resizing window
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def draw_location(self, loc_str, colorcode):
        loc = self.locationdict[loc_str]
        node = self.G.get_node_for_location(loc)
        x = node.position.x
        y = node.position.y
        line, = self.ax.plot(x, y, 'D', c=colorcode)
        self.canvas.draw()
        return line

    def draw_startloc(self, event):
        ''' Mark the selected start location in the graph '''
        # Remove previously marked start location
        if hasattr(self, 'startloc_plot'):
            self.startloc_plot.remove()
        self.remove_path_plot()
        start_str = self.start_combobox.get()
        self.startloc_plot = self.draw_location(start_str, 'g')

    def draw_endloc(self, event):
        ''' Mark the selected end location in the graph '''
        # Remove previously marked end location
        if hasattr(self, 'endloc_plot'):
            self.endloc_plot.remove()
        self.remove_path_plot()
        start_str = self.end_combobox.get()
        self.endloc_plot = self.draw_location(start_str, 'r')

    def draw_graph(self):
        ''' Draw all locations and connections '''
        # Plot edges
        for _, node in self.nodedict.items():
            x0 = node.position.x
            y0 = node.position.y
            # Loop node edges
            for edge in node.edges:
                # Get to-node
                tonode = self.nodedict[edge.to_node]
                x1 = tonode.position.x
                y1 = tonode.position.y
                self.ax.plot([x0, x1], [y0, y1], 'k-')
        # Plot nodes
        node_positions = [n.position for n in self.nodedict.values()]
        x = [n.x for n in node_positions]
        y = [n.y for n in node_positions]
        self.ax.plot(x, y, 'o', c='lightgray')
        # Update canvas
        self.canvas.draw()

    def get_route(self):
        ''' Calculate distance and draw path '''
        self.remove_path_plot()
        route = self.get_shortest_path()
        self.draw_path(route.path)

    def remove_path_plot(self):
        ''' Remove previous shortest path from figure '''
        if hasattr(self, 'path_plot_list'):
            for plotobj in self.path_plot_list:
                plotobj.remove()
                self.path_plot_list = []

    def get_shortest_path(self):
        ''' Calculate the shortest path between the start and end locations '''
        # Get start node ID for start location
        start_str = self.start_combobox.get()
        start_loc = self.locationdict[start_str]
        start_node = self.G.get_node_id_for_location(start_loc)

        # Get end node ID for end location
        end_str = self.end_combobox.get()
        end_loc = self.locationdict[end_str]
        end_node = self.G.get_node_id_for_location(end_loc)

        # Get shortest path
        po = PathFinder()
        route = po.shortest_path(self.G, start_node, end_node)
        self.distvar.set('{:.1f}'.format(route.cost))
        return route

    def draw_path(self, path):
        ''' Draw the path on the map '''
        # Get list of positions for the path nodes
        path_node_dict = {k: self.nodedict[k] for k in path}
        node_positions = [n.position for n in path_node_dict.values()]
        x = [n.x for n in node_positions]
        y = [n.y for n in node_positions]
        self.path_plot_list = []
        # Draw nodes except start and end node
        nodes_plot, = self.ax.plot(x[1:-1], y[1:-1], 'bo')
        self.path_plot_list.append(nodes_plot)
        # Draw edges
        for i in range(len(x)-1):
            edge_plot, = self.ax.plot([x[i], x[i+1]], [y[i], y[i+1]], 'b-')
            self.path_plot_list.append(edge_plot)
        # Update canvas
        self.canvas.draw()


if __name__ == '__main__':

    root = Tk()
    root.title("Warehouse Route")
    obj = WarehouseRouteGUI(root)
    root.mainloop()
