import lancedb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

from config import DB_PATH, TABLE_NAME, GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)

llm = genai.GenerativeModel("gemini-1.5-pro")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

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

If answer is not present, say:
"I could not find this information in the documents."

Context:
{context}

Question:
{question}
"""

    response = llm.generate_content(prompt)

    return response.text


while True:

    question = input("\nAsk Question: ")

    if question.lower() == "exit":
        break

    answer = ask_question(question)

    print("\nAnswer:")
    print(answer)