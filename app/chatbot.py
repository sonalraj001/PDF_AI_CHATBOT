import lancedb
from sentence_transformers import SentenceTransformer
from google import genai

from config import DB_PATH, TABLE_NAME, GEMINI_API_KEY


# Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect LanceDB
db = lancedb.connect(DB_PATH)

table = db.open_table(TABLE_NAME)


def retrieve_context(query, top_k=3):

    query_embedding = embedding_model.encode(query).tolist()

    results = (
        table.search(query_embedding)
        .limit(top_k)
        .to_list()
    )

    context = "\n".join([r["text"] for r in results])

    return context


def ask_question(question):

    context = retrieve_context(question)

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

If answer is not present in context, say:
'I could not find this information in the documents.'

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text


while True:

    question = input("\nAsk Question: ")

    if question.lower() == "exit":
        break

    answer = ask_question(question)

    print("\nAnswer:")
    print(answer)