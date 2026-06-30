from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

import pandas as pd
import os


load_dotenv()


# =========================
# LOAD VECTOR DATABASE
# =========================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embedding_model
)


# =========================
# LOAD DYNAMIC DATA
# =========================

dynamic_data = pd.read_csv(
    "data/dynamic/parking_dynamic.csv"
)


# =========================
# LOAD LLM
# =========================

llm = ChatOpenAI(
    model="meta-llama/llama-3.1-8b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3
)


# =========================
# PROMPT TEMPLATE
# =========================

prompt = ChatPromptTemplate.from_template("""
You are an intelligent parking assistant.

Use ONLY the provided context.

Context:
{context}

Question:
{question}

Answer professionally.
""")


# =========================
# SECURITY GUARDRAILS
# =========================

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "database password",
    "admin credentials",
]


def detect_prompt_injection(user_input):

    lower_input = user_input.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in lower_input:
            return True

    return False


# =========================
# RETRIEVAL FUNCTION
# =========================

def retrieve_context(query):

    results = vector_db.similarity_search(
        query,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    return context


# =========================
# AVAILABILITY FUNCTION
# =========================

def check_availability():

    available = dynamic_data[
        dynamic_data["slot_type"] == "Standard"
    ]["available_slots"].values[0]

    return f"{available} Standard slots available."


# =========================
# CHATBOT FUNCTION
# =========================

def parking_chatbot(user_query):

    if detect_prompt_injection(user_query):

        return (
            "Security warning: "
            "Request blocked."
        )

    if "availability" in user_query.lower():

        return check_availability()

    context = retrieve_context(user_query)

    formatted_prompt = prompt.format(
        context=context,
        question=user_query
    )

    response = llm.invoke(
        formatted_prompt
    )

    return response.content


# =========================
# TERMINAL INTERFACE
# =========================

def run_chatbot():

    print("\n" + "="*50)
    print(" SMART PARKING AI ASSISTANT ")
    print("="*50)

    print("\nType 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":

            print("\nGoodbye!\n")
            break

        response = parking_chatbot(
            user_input
        )

        print(f"\nBot: {response}\n")


if __name__ == "__main__":

    run_chatbot()