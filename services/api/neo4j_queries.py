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

        MATCH (tom:Person {name:"Tom Hanks"})
        RETURN tom
        """,
        database_="neo4j",
        )
        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
    ))

    @staticmethod
    def specific_movie(driver: Driver):
        records, summary, keys = driver.execute_query("""
        MATCH (cloudAtlas:Movie )
        WHERE cloudAtlas.title = "Cloud Atlas"
        RETURN cloudAtlas
        """,
        database_="neo4j",
        )

        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))

    @staticmethod
    def limit_result_person(driver : Driver, limit: int):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person)
        RETURN p.name LIMIT 10
        """)
        
        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def return_specific_property(driver: Driver):
        records, summary, keys = driver.execute_query("""
        MATCH (nineties:Movie)
        WHERE nineties.released = 1990
        RETURN nineties.title
        """)
        
        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod 
    def eighties_movies(driver: Driver):
        records, summary, keys = driver.execute_query("""
        MATCH (m:Movie)
        WHERE m.released > 1990 and m.released < 2000  
        RETURN m.title, m.released
        LIMIT 5
        """)
        
        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))

    @staticmethod
    def all_hanks_movies(driver: Driver):
        records, summary, keys = driver.execute_query(
        """
        MATCH(hanks:Person {name: "Tom Hanks"})-[r]->(tomHanksMovies:Movie)
        RETURN tomHanksMovies.title
        LIMIT 5
        """
        )

        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))

    @staticmethod
    def cloud_atlas_reals(driver: Driver):
        records, summary, key =driver.execute_query(
            """
        MATCH(directors)-[directed]->(m:Movie {title:"Cloud Atlas"})
        RETURN directors.name
        LIMIT 5
        """
        )

        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def tom_hanks_co_actors(driver: Driver):
        records, summary, key =driver.execute_query(
            """
        MATCH(p:Person {name: "Tom Hanks"})-[a:ACTED_IN]->(m:Movie)<-[b:ACTED_IN]-(co_actors:Person)
        RETURN co_actors.name
        LIMIT 5
        """
        )

        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def cloud_atlas_related_persons(driver: Driver):
        records, summary, keys= driver.execute_query(
            """
        MATCH (people:Person)-[relatedTo]-(:Movie {title: "Cloud Atlas"})
        RETURN people.name, type(relatedTo), relatedTo
        """
        )
        for record in records:
            print(record.data()) 

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def connected_to_bacon(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH p=(bacon:Person {name: "Kevin Bacon"})-[*1..3]-(a:Person)
        RETURN DISTINCT bacon, a, p
        LIMIT 10
        """
        )

        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def find_shortest_path(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH p=shortestPath(
            (bacon:Person {name: "Kevin Bacon"})-[*]-(meg:Person {name: "Meg Ryan"})
        )
        RETURN p
        LIMIT 10
        """
        )

        for record in records:
            print(record.data())

        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def cast_of_matrix(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH(movie:Movie {title: "The Matrix"})<-[:ACTED_IN]-(actors:Person)
        RETURN actors.name
        """
        )

        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def co_actor(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH(actor:Person {name: "Keanu Reeves"})-[a:ACTED_IN]->(m:Movie)<-[b:ACTED_IN]-(coActors: Person)
        RETURN a,b,m.title, coActors.name
        LIMIT 2
        """
        )

        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def acted_and_directed(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH(p:Person)-[a:ACTED_IN]->(m:Movie)<-[b:DIRECTED]-(p)
        RETURN p
        LIMIT 4
        """
        )

        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def hops_4_actors(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH p = (a:Person {name: "Tom Hanks"})-[*4]-(x:Person {name: "Kevin Bacon"})
        RETURN p
        LIMIT 2
        """
        )
        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def shortest_bridge_keenu_hanks(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH s=shortestPath((p:Person {name:"Keanu Reeves"})-[*1..10]-(x:Person {name: "Tom Hanks"}))
        RETURN s
        """
        )
        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def keanu_hanks_excluding_critics(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
            MATCH x=shortestPath((p:Person {name:"Keanu Reeves"})-[:ACTED_IN|PRODUCED|DIRECTED*1..10]-(h:Person {name: "Tom Hanks"}))
            RETURN x
        """
        )

        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def hanks_before_2000(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
            MATCH(p:Person {name: "Tom Hanks"})-[ACTED_IN]->(m:Movie)
            WHERE m.released > 2000
            RETURN m.title
        """
        )

        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def set_cloud_atlas_rating(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH(m:Movie {title: "Cloud Atlas" })
        SET m.rating = 5
        RETURN m.title, m.rating
        """
        )
        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    
    @staticmethod
    def update_matrix_version(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH(m:Movie {title: "The Matrix" })
        WHERE m.version IS NULL
        SET m.version = "Remastered"
        RETURN m.title, m.version
        """
        )
        for record in records:
            print(record.data())
        
        return("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))
    






    

        
 

    @staticmethod
    def update_embeddings(driver: Driver):
        records, _, _ = driver.execute_query(
            "MATCH (p:Person) WHERE p.embedding IS NULL RETURN p.name AS name",
            database_="sandbox.training"
        )
        
        print(f"Found {len(records)} persons to embed...")

        for record in records:
            name = record["name"]
            print(f"Embedding {name}...")
            
            vector = create_graph_embeddings(name)
            
            driver.execute_query(
                "MATCH (p:Person {name: $name}) SET p.embedding = $vector",
                name=name, vector=vector,
                database_="sandbox.training"
            )
        if records:
            return dict(records[0]["p"].items())
        return None
    


    @staticmethod
    def create_knowledge_graph_nodes(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        CREATE(bob:Employee {name: "Bob"})
        CREATE(alice:Employee {name: "Alice"})
        CREATE(work1:Device {name: "work_01"})
        CREATE(work2:Device {name:"work_02"})
        CREATE(malware:File {name:"malware"})
        CREATE(folder:Folder {name:"Project_x_share"})
        """
        )

        for record in records:
            print(record.data())

    @staticmethod
    def create_knowledge_graph_relationships(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH(p:Employee {name: "Alice"})
        MATCH(e:Device {name: "work_01"})
        MERGE((p)-[r:owns]->(e))
        MATCH(pe:Employee {name: "Bob"})
        MATCH(t:Device {name: "work_02"})
        MERGE((pe)-[:owns]->(t))
        MATCH(device:Device {name: "work_01"})
        MATCH(folder:Folder {name: "Project_x_share"})
        MERGE((device)-[mount:mounted]->(folder))
        MATCH(device2:Device {name: "work_02"})
        MATCH(folder2:Folder {name: "Project_x_share"})
        MERGE((device2)-[:mounted]->(folder2))
        """
        )

        for record in records:
            print(record.data())
        
    @staticmethod
    def delete_relationship(driver: Driver):
        records, summary, keys = driver.execute_query(
            """
        MATCH(p:Device {name:"work_02"})-[r:mount]->()
        DELETE r
        """
        )

        for record in records:
            print(record.data())
        

