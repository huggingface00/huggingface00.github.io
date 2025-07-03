# from pygraphviz import AGraph

# DOT_FILE = "graph.dot"
# OUTPUT_CYPHER = "import.cypher"

# def main():
#     # Load the .dot file
#     g = AGraph(DOT_FILE)

#     cypher_statements = []

#     # First, MERGE all nodes
#     for node in g.nodes():
#         node_id = node.get_name().strip('"')  # get numeric ID or name
#         label = node.attr.get('label', 'Node').replace('"', "'")  # fallback label
#         cypher = (
#             f"MERGE (n:Dataset {{ id: '{node_id}' }}) "
#             f"SET n.name = '{label}'"
#         )
#         cypher_statements.append(cypher)

#     # Then, MERGE all edges
#     for edge in g.edges():
#         source_id = edge[0].strip('"')
#         target_id = edge[1].strip('"')
#         rel_label = edge.attr.get('label', 'RELATED_TO').replace('"', "'")
#         cypher = (
#             f"MATCH (a:Dataset {{ id: '{source_id}' }}), "
#             f"(b:Dataset {{ id: '{target_id}' }}) "
#             f"MERGE (a)-[:{rel_label}]->(b)"
#         )
#         cypher_statements.append(cypher)

#     # Write all statements to the output file
#     with open(OUTPUT_CYPHER, "w") as f:
#         for stmt in cypher_statements:
#             f.write(stmt + "\n")

#     print(f"✅ Cypher script written to {OUTPUT_CYPHER}")

# if __name__ == "__main__":
#     main()

import re

# Point to your DOT file with precomputed edges
INPUT_DOT = "precomputed_edges_apr_30.dot"
OUTPUT_CYPHER = "import_1000.cypher"

# Regex patterns
node_pattern = re.compile(r'"?(\d+)"?\s*\[label="([^"]+)"\]')
edge_pattern = re.compile(r'"?(\d+)"?\s*->\s*"?(\d+)"?\s*(?:\[label="([^"]*)"\])?')

nodes = {}
edges = []

with open(INPUT_DOT) as f:
    for line in f:
        m_edge = edge_pattern.search(line)
        if m_edge:
            src, tgt, label = m_edge.groups()
            label = label or ""  # handle cases with no label
            edges.append((src, tgt, label))
            nodes[src] = None  # will fill names if available later
            nodes[tgt] = None
            continue

        m_node = node_pattern.search(line)
        if m_node:
            node_id, name = m_node.groups()
            nodes[node_id] = name

# Take the first 1000 edges
edges = edges[:1000]

# Collect only nodes used in those edges
used_node_ids = set()
for src, tgt, _ in edges:
    used_node_ids.add(src)
    used_node_ids.add(tgt)

with open(OUTPUT_CYPHER, "w") as f:
    # MERGE nodes
    for node_id in sorted(used_node_ids):
        name = nodes.get(node_id) or ""
        name_str = f'"{name}"'
        f.write(f'MERGE (n:Dataset {{id: "{node_id}"}}) SET n.name = {name_str};\n')

    # MERGE relationships
    for src, tgt, label in edges:
        label_str = f'type: "{label}"' if label else ''
        if label_str:
            rel_props = f'{{ {label_str} }}'
        else:
            rel_props = ''
        f.write(
            f'MATCH (a:Dataset {{id: "{src}"}}), (b:Dataset {{id: "{tgt}"}}) '
            f'MERGE (a)-[:TRAINED_ON {rel_props}]->(b);\n'
        )

print(f"✅ Cypher script written to {OUTPUT_CYPHER} with {len(used_node_ids)} nodes and {len(edges)} edges.")
