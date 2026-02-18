from services.api.endpoints import create_graph_relations,know_persons
from services.config import start_neo4j_connection
from dotenv import load_dotenv

load_dotenv()

def main():
    neo4j_driver = start_neo4j_connection()
    if neo4j_driver:
        try:
            create_graph_relations(neo4j_driver, "victor", "tony")
            know_persons(neo4j_driver)

        finally:
                neo4j_driver.close()
                print("🔌 Driver closed.")


if __name__ == "__main__":
    main()