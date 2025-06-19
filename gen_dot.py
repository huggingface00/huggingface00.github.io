import pandas as pd
import html

nodes = pd.read_csv("nodes.csv").head(100)
edges = pd.read_csv("edges.csv").head(100)

with open("graph.dot", "w") as f:
    f.write("digraph G {\n")

    # Add nodes
    for _, row in nodes.iterrows():
        label = html.escape(str(row["name"]).replace('"', ''))
        f.write(f'  {row["node_id"]} [label="{label}"];\n')

    # Add edges
    for _, row in edges.iterrows():
        edge_label = html.escape(str(row["edge_type"]).replace('"', ''))
        f.write(f'  {row["Source"]} -> {row["Target"]} [label="{edge_label}"];\n')

    f.write("}")
