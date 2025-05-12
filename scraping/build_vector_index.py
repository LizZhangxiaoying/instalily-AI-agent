
import os
import json
from openai import OpenAI
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# load data files
data_dir = os.path.join(os.path.dirname(__file__), "data")
files = ["mock_refrigerator_parts.json", "mock_dishwasher_parts.json"]

parts = []
for file in files:
    with open(os.path.join(data_dir, file), "r") as f:
        parts.extend(json.load(f))

# format text for embeddings
def format_part(p):
    return f"Title: {p['title']}\nDescription: {p['description']}\nInstallation: {p['installation']}\nTroubleshooting: {p['troubleshooting']}"

texts = [format_part(p) for p in parts]

# ask OpenAI API to generate embeddings
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

embeddings = [get_embedding(text) for text in texts]
embeddings = np.array(embeddings).astype("float32")

# create FAISS index
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

# Save the index and metadata
faiss.write_index(index, os.path.join(data_dir, "parts_index.faiss"))

with open(os.path.join(data_dir, "parts_metadata.json"), "w") as f:
    json.dump(parts, f, indent=2)

