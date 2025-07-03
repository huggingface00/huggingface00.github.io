from flask import Flask, jsonify, send_from_directory
from neo4j import GraphDatabase

# Neo4j connection
driver = GraphDatabase.driver(
    "bolt://localhost:7687", 
    auth=("neo4j", "neo4j123")
)

app = Flask(__name__, static_folder=".")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/graph")
def get_graph():
    session = driver.session()
    query = """
        MATCH (n:Dataset)-[r:TRAINED_ON]->(m:Dataset)
        RETURN n, r, m
        LIMIT 100
    """
    result = session.run(query)
    nodes = []
    links = []
    node_ids = set()

    for record in result:
        n = record["n"]
        m = record["m"]
        r = record["r"]

        for node in [n, m]:
            node_id = str(node.id)
            if node_id not in node_ids:
                nodes.append({
                    "id": node_id,
                    "label": node.labels.pop() if node.labels else "Node",
                    "properties": node._properties
                })
                node_ids.add(node_id)

        links.append({
            "source": str(n.id),
            "target": str(m.id),
            "type": r.type
        })

    session.close()
    return jsonify({"nodes": nodes, "links": links})

if __name__ == "__main__":
    app.run(debug=True)
