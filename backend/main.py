
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_utils import search_similar_parts
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# 允许跨域（连接 React 前端 ）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求格式
class ChatRequest(BaseModel):
    user_message: str
    chat_history: list[str]  # Add this
    context: str

@app.post("/chat")
@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.user_message

    # vector search
    similar_parts = search_similar_parts(user_input, top_k=3)

    # construct context
    context_text = ""
    for part in similar_parts:
        context_text += f"Part: {part['title']}\n"
        context_text += f"Description: {part['description']}\n"
        context_text += f"Installation: {part['installation']}\n"
        context_text += f"Troubleshooting: {part['troubleshooting']}\n"
        context_text += f"Models: {', '.join(part['compatible_models'])}\n---\n"

    # construct chat history
    messages = [
        {
            "role": "system",
            "content": """You are a helpful and friendly assistant for the PartSelect website.
You specialize in helping users with refrigerator and dishwasher parts,
including installation guidance, part compatibility, and common troubleshooting.

If the user's question can be answered using the context below, do so precisely.

If the user's question is about general appliance troubleshooting (e.g., ice maker not working),
and the context is not sufficient, use your general knowledge to give clear, helpful,
step-by-step guidance. Keep your tone friendly and professional."""
        }
    ]

    for line in request.chat_history:
        if line.startswith("user:"):
            messages.append({ "role": "user", "content": line.replace("user:", "").strip() })
        elif line.startswith("assistant:"):
            messages.append({ "role": "assistant", "content": line.replace("assistant:", "").strip() })

    # Append the current user question and context
    messages.append({ "role": "user", "content": f"{context_text}\n\nCurrent question: {user_input}" })

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message.content
        return { "reply": answer }

    except Exception as e:
        return { "reply": "Sorry, something went wrong with the assistant." }
