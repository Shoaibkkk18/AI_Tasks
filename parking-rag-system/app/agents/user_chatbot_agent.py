import json
import os
import pandas as pd

from datetime import datetime

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_community.vectorstores import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from app.agents.reservation_agent import (
    collect_reservation_details
)

from app.agents.state_manager import (
    reservation_state
)


# =========================================
# LOAD ENVIRONMENT
# =========================================

load_dotenv()


# =========================================
# VECTOR DATABASE
# =========================================

embedding_model = HuggingFaceEmbeddings(
    model_name=(
        "sentence-transformers/"
        "all-MiniLM-L6-v2"
    )
)

vector_db = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embedding_model
)


# =========================================
# DYNAMIC DATA
# =========================================

dynamic_data = pd.read_csv(
    "data/dynamic/parking_dynamic.csv"
)


# =========================================
# LLM
# =========================================

llm = ChatOpenAI(
    model="meta-llama/llama-3.1-8b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3
)


# =========================================
# PROMPT
# =========================================

prompt = ChatPromptTemplate.from_template("""
You are an intelligent parking assistant.

Use ONLY the provided context.

Context:
{context}

Question:
{question}

Answer professionally.
""")


# =========================================
# SECURITY FILTER
# =========================================

BLOCKED_PATTERNS = [

    "ignore previous instructions",

    "reveal system prompt",

    "database password",

    "admin credentials"
]


def detect_prompt_injection(
    user_input
):

    lower_input = user_input.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in lower_input:
            return True

    return False


# =========================================
# RAG RETRIEVAL
# =========================================

def retrieve_context(query):

    results = vector_db.similarity_search(
        query,
        k=3
    )

    context = "\n\n".join(

        [
            doc.page_content
            for doc in results
        ]
    )

    return context


# =========================================
# AVAILABILITY
# =========================================

def check_availability():

    available = dynamic_data[
        dynamic_data["slot_type"] == "Standard"
    ]["available_slots"].values[0]

    return (
        f"{available} "
        f"Standard parking slots available."
    )


# =========================================
# RESERVATION STORAGE
# =========================================

PENDING_FILE = (
    "data/reservations/"
    "pending_reservations.json"
)


def generate_reservation_id():

    current_year = datetime.now().year

    with open(PENDING_FILE, "r") as file:

        pending = json.load(file)

    reservation_number = (
        len(pending) + 1
    )

    return (
        f"RES-"
        f"{current_year}-"
        f"{reservation_number:04d}"
    )


def save_reservation_request():

    with open(PENDING_FILE, "r") as file:

        data = json.load(file)

    reservation_state[
        "reservation_id"
    ] = generate_reservation_id()

    reservation_state[
        "created_at"
    ] = str(datetime.now())

    data.append(
        dict(reservation_state)
    )

    with open(PENDING_FILE, "w") as file:

        json.dump(data, file, indent=4)


# =========================================
# RESET RESERVATION STATE
# =========================================

def reset_reservation_state():

    reservation_state["first_name"] = None
    reservation_state["last_name"] = None
    reservation_state["verification_type"] = None
    reservation_state["verification_id"] = None
    reservation_state["car_number"] = None
    reservation_state["start_date"] = None
    reservation_state["end_date"] = None
    reservation_state["status"] = "pending"


# =========================================
# RESERVATION WORKFLOW
# =========================================

def start_reservation_flow():

    reset_reservation_state()

    print("\n" + "="*60)

    print(" RESERVATION WORKFLOW ")

    print("="*60)

    response = collect_reservation_details()

    while True:

        print(f"\nBot: {response}")

        if (
            "completed"
            in response.lower()
        ):

            break

        user_input = input(
            "\nYou: "
        )

        response = collect_reservation_details(
            user_input
        )

    save_reservation_request()

    print(
        "\nBot: Reservation submitted "
        "for administrator approval.\n"
    )


# =========================================
# MAIN CHATBOT RESPONSE
# =========================================

def chatbot_response(user_query):

    # =====================================
    # SECURITY
    # =====================================

    if detect_prompt_injection(
        user_query
    ):

        return (
            "Security warning: "
            "Request blocked."
        )

    # =====================================
    # RESERVATION FLOW
    # =====================================

    reservation_keywords = [

        "reserve",

        "reservation",

        "book parking",

        "booking"
    ]

    if any(

        keyword in user_query.lower()

        for keyword in reservation_keywords

    ):

        start_reservation_flow()

        return (
            "Reservation workflow completed."
        )

    # =====================================
    # AVAILABILITY
    # =====================================

    if (
        "availability"
        in user_query.lower()
    ):

        return check_availability()

    # =====================================
    # RAG RESPONSE
    # =====================================

    context = retrieve_context(
        user_query
    )

    formatted_prompt = prompt.format(

        context=context,

        question=user_query
    )

    response = llm.invoke(
        formatted_prompt
    )

    return response.content