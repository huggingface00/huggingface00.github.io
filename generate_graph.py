from pyvis.network import Network
import networkx as nx
import pydot

graphs = pydot.graph_from_dot_file("graph.dot")
if not graphs:
    raise ValueError("No graphs found in DOT file.")
dot_graph = graphs[0]

# Convert pydot graph to networkx graph manually
nx_graph = nx.DiGraph()

# Add nodes
for node in dot_graph.get_nodes():
    node_name = node.get_name().strip('"')
    if node_name not in ['node', 'edge', 'graph']:
        nx_graph.add_node(node_name)

# Add edges
for edge in dot_graph.get_edges():
    source = edge.get_source().strip('"')
    target = edge.get_destination().strip('"')
    nx_graph.add_edge(source, target)

net = Network(height="750px", width="100%", directed=True)
net.from_nx(nx_graph)
net.toggle_physics(True)
net.show_buttons(filter_=['physics'])
net.save_graph("graph_visualization.html")