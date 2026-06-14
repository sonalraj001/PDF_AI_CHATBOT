import lancedb
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from utils import load_documents
from config import DB_PATH, TABLE_NAME, DOCUMENTS_PATH


model = SentenceTransformer('all-MiniLM-L6-v2')

db = lancedb.connect(DB_PATH)

documents = load_documents(DOCUMENTS_PATH)

chunks = []

CHUNK_SIZE = 500

print(documents)

for doc in documents:

    text = doc["text"]

    for i in range(0, len(text), CHUNK_SIZE):

        chunk = text[i:i + CHUNK_SIZE]

        embedding = model.encode(chunk).tolist()

        chunks.append({
            "text": chunk,
            "source": doc["filename"],
            "vector": embedding
        })

df = pd.DataFrame(chunks)

table = db.create_table(TABLE_NAME, data=df, mode="overwrite")

print("Documents ingested successfully!")