# import csv

# INPUT_CSV = "nodes_Apr_30.csv"
# OUTPUT_DOT = "graph_nodes_only.dot"

# with open(INPUT_CSV, newline='', encoding="utf-8") as csvfile:
#     reader = csv.DictReader(csvfile)
#     nodes = []
#     for row in reader:
#         node_id = row["node_id"].strip()
#         name = row["name"].strip()
#         nodes.append((node_id, name))

# with open(OUTPUT_DOT, "w") as f:
#     f.write("digraph {\n")
#     for node_id, name in nodes:
#         f.write(f'    "{node_id}" [label="{name}"];\n')
#     f.write("}\n")

# print(f"✅ DOT file written to {OUTPUT_DOT} with {len(nodes)} nodes")

INPUT_DOT = "graph_nodes_only.dot"
OUTPUT_DOT = "graph_1000.dot"

subset_lines = []
with open(INPUT_DOT) as f:
    lines = f.readlines()

# Keep header and footer
header = lines[0]
footer = lines[-1]
edge_lines = lines[1:-1]

# Take first 1000 edges
subset = edge_lines[:1000]

with open(OUTPUT_DOT, "w") as f:
    f.write(header)
    f.writelines(subset)
    f.write(footer)

print(f"✅ 100k edge DOT file written to {OUTPUT_DOT}")
