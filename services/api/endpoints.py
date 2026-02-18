from neo4j import GraphDatabase, Driver


def create_graph_relations(driver: Driver, name: str, friendName: str):
     summary = driver.execute_query("""
                CREATE (a:Person {name: $name})
                CREATE (b:Person {name: $friendName})
                CREATE (a)-[:KNOWS]->(b)
                """,
                name=name, friendName=friendName,
                database_="relationship.finder",
            ).summary
     print("Created {nodes_created} nodes in {time} ms.".format(
                nodes_created=summary.counters.nodes_created,
                time=summary.result_available_after
            ))
     


def know_persons(driver : Driver):
    records, summary, keys = driver.execute_query("""
    MATCH (p:Person)-[:KNOWS]->(:Person)
    RETURN p.name AS name
    """,
    database_="relationship.finder",)
    
    for record in records:
        print(record.data()) 

    print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after
))

def update_object(driver: Driver, name: str, age: int):
    records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    SET p.age = $age
    """, name=name, age=age,
    database_="relationship.finder",
    )
    print(f"Query counters: {summary.counters}.")
