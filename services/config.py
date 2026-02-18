import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME", "neo4j") 
PASSWORD = os.getenv("NEO4J_PASSWORD")

def start_neo4j_connection():
    try:
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        
        driver.verify_connectivity()

        print(f"neo4J driver initialized")
        
        return driver
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")