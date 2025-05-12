
import os
import json
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# load FAISS index and metadata
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scraping", "data"))
INDEX_PATH = os.path.join(DATA_DIR, "parts_index.faiss")
METADATA_PATH = os.path.join(DATA_DIR, "parts_metadata.json")

index = faiss.read_index(INDEX_PATH)
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

def get_query_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return np.array(response.data[0].embedding).astype("float32")

def search_similar_parts(query, top_k=3):
    query_vec = get_query_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_vec, top_k)
    return [metadata[i] for i in indices[0]]
