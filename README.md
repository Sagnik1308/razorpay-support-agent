🏦 Razorpay Support AI Agent

An AI-powered customer-support assistant for a mid-sized fintech company (inspired by Razorpay).
The agent answers customer queries using a knowledge base built from the Razorpay Docs and allows users to escalate unresolved questions to a human agent via Google Sheets.

🚀 Features

RAG-based response system: Uses OpenAI embeddings + FAISS vector search to answer questions from Razorpay documentation.

FastAPI backend: Serves endpoints for chat, feedback, and health checks.

Google Sheets integration: Automatically logs user name, email, and query when they request human support.

Frontend chat UI: Simple HTML, CSS, and JS interface for interactive Q&A.

Deployed on cloud (Render / Railway): End-to-end functional deployment.

🧠 Tech Stack
Layer	Tools Used
Language	Python
Framework	FastAPI
Vector Search	FAISS-CPU
LLM Integration	OpenAI GPT-4o-mini
Data Storage	Google Sheets API
Frontend	HTML, CSS, JavaScript
Deployment	Render (switchable to Railway)
📁 Project Structure
razorpay-support-agent/
│
├── backend/
│   ├── server.py          # FastAPI server (chat + feedback APIs)
│   ├── models.py          # Pydantic models for request/response
│   ├── rag.py             # RAG pipeline (embedding + retrieval)
│   ├── prompts.py         # System and answer prompt templates
│   ├── sheets_utils.py    # Google Sheets integration
│   ├── ingest.py          # Builds FAISS index from Razorpay docs
│   └── .env.example       # Example environment variables
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── render.yaml            # Render deployment config

⚙️ Environment Variables
Variable	Description
OPENAI_API_KEY	Your OpenAI API key
EMBEDDING_MODEL	text-embedding-3-small
CHAT_MODEL	gpt-4o-mini
GOOGLE_SHEETS_SPREADSHEET_NAME	Google Sheet name for feedback logs
GOOGLE_SERVICE_ACCOUNT_JSON	Path to service account key file
PORT	Default 8000
FINTECH_BRAND	“Razorpay”
🧩 API Endpoints
Endpoint	Method	Description
/health	GET	Sanity check
/chat	POST	Get AI response to a user query
/feedback	POST	Log user details in Google Sheet
💬 Example

Request:

{
  "session_id": "123",
  "message": "How long does Razorpay settlement take?"
}


Response:

{
  "answer": "Razorpay settlements typically take T+2 days...",
  "sources": [{"url": "https://razorpay.com/docs/payments/settlements/"}],
  "suggested_quick_replies": ["Refund timelines", "KYC requirements"]
}

🌐 Deployment

Backend: FastAPI on Render / Railway

Frontend: Served from same app root

Knowledge Base: Embedded from Razorpay Docs

🧰 Setup (Local)
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python ingest.py  # builds embeddings
uvicorn backend.server:app --reload


Then open frontend/index.html in browser.
