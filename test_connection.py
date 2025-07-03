from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=None)

with driver.session() as session:
    result = session.run("RETURN 1 AS test")
    print("✅ Connected successfully:", result.single()["test"])
