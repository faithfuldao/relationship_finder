from neo4j import GraphDatabase, Driver

class Neo4J_Queries:
    @staticmethod
    def create_graph_relations(driver: Driver, name: str, friendName: str):
        summary = driver.execute_query("""
                CREATE (a:Person {name: $name})
                CREATE (b:Person {name: $friendName})
                CREATE (a)-[:KNOWS]->(b)
                """,
                name=name, friendName=friendName,
                database_="relationship.finder",
            ).summary
        return("Created {nodes_created} nodes in {time} ms.".format(
                nodes_created=summary.counters.nodes_created,
                time=summary.result_available_after
            ))
     

    @staticmethod
    def know_persons(driver : Driver):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person)-[:KNOWS]->(:Person)
        RETURN p.name AS name
        """,
        database_="relationship.finder",)
        
        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
    ))

    @staticmethod
    def update_object(driver: Driver, name: str, age: int):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.age = $age
        """, name=name, age=age,
        database_="relationship.finder",
        )
        return(f"Query counters: {summary.counters}.")

    @staticmethod
    def get_user_age(driver:Driver):
        records, summary, keys = driver.execute_query(
        "MATCH (p:Person) RETURN p.name AS name, p.age AS age",
        routing_="r",
        database_="relationship.finder",)

        users_name = []
        
        for record in records:
            users_name.append(record.data())
        
        return users_name

