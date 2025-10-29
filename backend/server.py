import os, requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.models import ChatRequest, ChatResponse, FeedbackRequest, Source
from backend.rag import retrieve
from backend.prompts import SYSTEM_PROMPT, ANSWER_PROMPT

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    hits = retrieve(req.message)
    context = "\n\n".join([f"[{i+1}] {h['text'][:800]}" for i, h in enumerate(hits)])
    prompt = ANSWER_PROMPT.format(context=context, question=req.message)

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": CHAT_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
    )
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail=r.text)

    answer = r.json()["choices"][0]["message"]["content"]
    sources = [Source(url=h["url"], score=h["score"]) for h in hits[:2]]
    return ChatResponse(
        answer=answer,
        sources=sources,
        suggested_quick_replies=["Refund timelines", "KYC requirements", "Talk to a human"],
        escalatable=True,
    )

from sheets_utils import append_to_sheet

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    try:
        append_to_sheet(req.name, req.email, req.question, req.session_id)
        return {"success": True, "message": "Feedback logged successfully"}
    except Exception as e:
        print("❌ Sheets error:", e)
        raise HTTPException(status_code=500, detail=str(e))

# --- Static frontend (serves /frontend as the site root) ---
from fastapi.staticfiles import StaticFiles
import os

frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")