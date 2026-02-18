from neo4j import GraphDatabase, Driver
from openai import OpenAI
from services.api.embeddings import create_graph_embeddings

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
    
    #same query the professional way
    @staticmethod
    def get_user_infos(driver:Driver):
        records, _, _ = driver.execute_query(
        "MATCH (p:Person) RETURN p{ .name, .age, .city } AS user_profile",
        database_="relationship.finder",
        )
        return [record["user_profile"] for record in records]
    
    #gets all the fields of the Object without having to type each one
    @staticmethod
    def get_all_user_infos(driver: Driver):
        records, _, _ = driver.execute_query(
            "MATCH (p:Person) RETURN p",
            routing_= 'r',
            database_="relationship.finder",
        )
        if records:
            # record["p"] is a Node object. 
            # .items() converts all properties into a dictionary automatically.
            return dict(records[0]["p"].items())
        return None
    
    @staticmethod
    def update_embeddings(driver: Driver):
        records, _, _ = driver.execute_query(
            "MATCH (p:Person) WHERE p.embedding IS NULL RETURN p.name AS name",
            database_="relationship.finder"
        )
        
        print(f"Found {len(records)} persons to embed...")

        for record in records:
            name = record["name"]
            print(f"Embedding {name}...")
            
            vector = create_graph_embeddings(name)
            
            driver.execute_query(
                "MATCH (p:Person {name: $name}) SET p.embedding = $vector",
                name=name, vector=vector,
                database_="relationship.finder"
            )
        if records:
            return dict(records[0]["p"].items())
        return None

