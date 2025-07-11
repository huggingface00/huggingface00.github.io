# from neo4j import GraphDatabase

# # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
# URI = "neo4j+s://72da2fde.databases.neo4j.io"
# AUTH = ("neo4j", "6OEkKBIcouM-Ngx6nIV1IXkDKsIBrKuvTIpVkB1730s")

# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     driver.verify_connectivity()

from neo4j import GraphDatabase

uri = "neo4j+s://72da2fde.databases.neo4j.io"
auth = ("neo4j", "iByx_b0QLYjEe9UyY4Kd3ez-RtHDXgT-CX8T_p8QEJU")

driver = GraphDatabase.driver(uri, auth=auth)

with driver.session() as session:
    result = session.run("RETURN 1")
    print(result.single())
