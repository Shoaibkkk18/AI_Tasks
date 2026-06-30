from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

import os
import pandas as pd

load_dotenv()

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/frontend/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/frontend/templates"
)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embedding_model
)

dynamic_data = pd.read_csv(
    "data/dynamic/parking_dynamic.csv"
)

llm = ChatOpenAI(
    model="meta-llama/llama-3.1-8b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3
)

prompt = ChatPromptTemplate.from_template("""
You are an intelligent parking assistant.

Use ONLY the provided context.

Context:
{context}

Question:
{question}
""")


class ChatRequest(BaseModel):
    message: str


def retrieve_context(query):

    results = vector_db.similarity_search(query, k=3)

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    return context


def check_availability():

    available = dynamic_data[
        dynamic_data["slot_type"] == "Standard"
    ]["available_slots"].values[0]

    return f"{available} Standard slots available."


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/chat")
async def chat(chat_request: ChatRequest):

    user_query = chat_request.message

    if "availability" in user_query.lower():
        return {
            "response": check_availability()
        }

    context = retrieve_context(user_query)

    formatted_prompt = prompt.format(
        context=context,
        question=user_query
    )

    response = llm.invoke(formatted_prompt)

    return {
        "response": response.content
    }