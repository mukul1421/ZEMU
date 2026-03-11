from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import chromadb
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import os
import time

# ---------------- Load Environment Variables ----------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT_ID = os.getenv("CHROMA_TENANT_ID")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")

app = Flask(__name__)

# ---------------- Chroma Cloud Setup ----------------
client = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT_ID,
    database=CHROMA_DATABASE
)

collection = client.get_or_create_collection(name="sikkim_guide")

# ---------------- Embedding Model ----------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- Groq Setup ----------------
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


# ---------------- Retrieve from Chroma ----------------
def retrieve_from_chroma(query, top_k=5, similarity_threshold=0.45):

    embedding = embed_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    docs = []

    if results and "documents" in results:

        documents = results["documents"][0]
        distances = results["distances"][0]

        for doc, distance in zip(documents, distances):

            if distance < similarity_threshold:
                docs.append(doc)

    return docs


# ---------------- Call Groq API ----------------
def generate_with_groq(prompt):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert Sikkim tourism guide. Give short, clear answers."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 200
    }

    for attempt in range(3):

        try:

            response = requests.post(
                GROQ_URL,
                headers=headers,
                json=data,
                timeout=20
            )

            if response.status_code == 429:
                time.sleep(2)
                continue

            response.raise_for_status()

            result = response.json()

            return result["choices"][0]["message"]["content"].strip()

        except Exception as e:

            if attempt == 2:
                return f"Error contacting Groq API: {str(e)}"

            time.sleep(2)


# ---------------- Format Context ----------------
def format_context(docs):

    context_text = ""

    for i, doc in enumerate(docs, 1):
        context_text += f"{i}. {doc}\n"

    return context_text


# ---------------- API CHAT ENDPOINT ----------------
@app.route("/api/chat", methods=["POST"])
def chat_api():

    try:

        data = request.get_json()

        user_query = data.get("text", "")
        lang = data.get("lang", "en")

        # Translate to English
        if lang != "en":

            try:
                translated_query = GoogleTranslator(
                    source=lang,
                    target="en"
                ).translate(user_query)

            except:
                translated_query = user_query

        else:
            translated_query = user_query

        # Retrieve RAG context
        retrieved_docs = retrieve_from_chroma(translated_query)

        if retrieved_docs:

            context = format_context(retrieved_docs)

            prompt = f"""
You are a Sikkim tourism assistant.

Answer ONLY using the context below.
If the answer is not in the context say:
"I couldn't find that information in my database."

Context:
{context}

Question:
{translated_query}

Answer in 2–3 clear sentences.
"""

        else:

            prompt = translated_query

        ai_reply_en = generate_with_groq(prompt)

        # Translate back
        if lang != "en":

            try:
                ai_reply = GoogleTranslator(
                    source="en",
                    target=lang
                ).translate(ai_reply_en)

            except:
                ai_reply = ai_reply_en

        else:
            ai_reply = ai_reply_en

        return jsonify({"response": ai_reply})

    except Exception as e:

        print("ERROR:", e)

        return jsonify({"response": "Server error occurred"})


# ---------------- Landing Page ----------------
@app.route("/")
def landing():

    return render_template("landing.html")


# ---------------- Chat Page ----------------
@app.route("/chat")
def chat_page():

    return render_template("chat.html")


# ---------------- Run Flask ----------------
if __name__ == "__main__":
    app.run(debug=True)