from services.api.neo4j_queries import Neo4J_Queries
from services.config import start_neo4j_connection
from dotenv import load_dotenv

load_dotenv()

def main():
    neo4j_driver = start_neo4j_connection()
    if neo4j_driver:
        try:
            #Neo4J_Queries.create_graph_relations(neo4j_driver, "victor", "tony")
            #Neo4J_Queries.know_persons(neo4j_driver)
            #Neo4J_Queries.update_object(neo4j_driver, "Victor", 34)
            users_age =Neo4J_Queries.get_user_infos(neo4j_driver)
            print(users_age)

        finally:
                neo4j_driver.close()
                print("Driver closed.")


if __name__ == "__main__":
    main()