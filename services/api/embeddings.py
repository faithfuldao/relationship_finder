from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_graph_embeddings(text: str):
    """Converts text into a 1536-dimensional vector."""
    
    if not text or not text.strip():
        print("⚠️ Warning: Skipping embedding for empty/null input.")
        return None

    clean_text = text.replace("\n", " ").strip()
    
    try:
        response = client.embeddings.create(
            input=[clean_text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    
    except Exception as e:
        print(f"❌ OpenAI Error for '{text}': {e}")
        return None
