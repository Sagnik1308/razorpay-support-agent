# 🏦 Razorpay Support AI Agent  

An AI-powered customer-support assistant for a mid-sized fintech company (inspired by Razorpay).  
The agent answers customer queries using a knowledge base built from the Razorpay Docs and allows users to escalate unresolved questions to a human agent via Google Sheets.  
---

## 🚀 Features
- **RAG-based response system:** Uses OpenAI embeddings + FAISS vector search to answer questions from Razorpay documentation.  
- **FastAPI backend:** Serves endpoints for chat, feedback, and health checks.  
- **Google Sheets integration:** Automatically logs user name, email, and query when they request human support.  
- **Frontend chat UI:** Simple HTML, CSS, and JS interface for interactive Q&A.  
- **Deployed on cloud (Render / Railway):** End-to-end functional deployment.  
---

## 🧠 Tech Stack

| Layer | Technology |
|--------|-------------|
| **Backend** | FastAPI, Python |
| **AI / NLP** | OpenAI API (GPT-4o-mini, text-embedding-3-small) |
| **Vector Store** | FAISS |
| **Database / Storage** | Google Sheets API |
| **Frontend** | HTML, CSS, JavaScript |
| **Deployment** | Render (or Railway) |
| **Environment** | Virtualenv, dotenv |
---

## 📂 Project Structure
```
razorpay-support-agent/
│
├── backend/
│   ├── server.py          # FastAPI app (main entry point)
│   ├── models.py          # Pydantic models for requests/responses
│   ├── rag.py             # Retrieval-Augmented Generation logic
│   ├── ingest.py          # Builds FAISS index from Razorpay docs
│   ├── sheets_utils.py    # Handles Google Sheets integration
│   ├── prompts.py         # System and answer prompts
│   ├── .env.example       # Example environment variables
│   └── requirements.txt   # Backend dependencies
│
├── frontend/
│   ├── index.html         # Chat interface
│   ├── script.js          # Handles API calls
│   └── style.css          # Styling for chat UI
│
└── README.md
```
---

## ⚙️ Setup & Run Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/razorpay-support-agent.git
cd razorpay-support-agent/backend
```

### 2️⃣ Create & Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # (Mac/Linux)
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` File
Copy `.env.example` → `.env` and fill in your credentials:
```
OPENAI_API_KEY=sk-xxxx
GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/service_account.json
GOOGLE_SHEETS_SPREADSHEET_NAME=Fintech Support Escalations
```

### 5️⃣ Build the Vector Index
```bash
python ingest.py
```

### 6️⃣ Run the Server
```bash
uvicorn backend.server:app --reload
```

### 7️⃣ Test API Endpoints
Visit:
- ✅ `/health` → Health check  
- 💬 `/chat` → Chat endpoint  
- 🧾 `/feedback` → Submit feedback  
---

## 🧩 API Endpoints Summary

| Endpoint | Method | Description |
|-----------|--------|--------------|
| `/health` | **GET** | Basic health check for the server |
| `/chat` | **POST** | Takes a user query, retrieves relevant context from Razorpay docs (via FAISS), and returns an AI-generated answer |
| `/feedback` | **POST** | Collects user name, email, and query, then logs the details into Google Sheets |
---

## ✨ Features Summary

- 🤖 **AI-Powered Chat Support:** Answers customer questions using a knowledge base built from Razorpay’s official documentation.  
- 💬 **Conversational Flow:** Maintains natural, human-like dialogue for smoother support interactions.  
- 📚 **Retrieval-Augmented Generation (RAG):** Uses FAISS-based document search + GPT reasoning to give accurate, contextual answers.  
- 📈 **Google Sheets Integration:** Escalated queries are automatically logged (with user name, email, and message).  
- ⚡ **Fast & Lightweight:** Built with FastAPI for quick responses and low latency.  
- 🧠 **Customizable Knowledge Base:** Can easily be trained on any fintech company’s docs or internal FAQs.  
- 🌐 **Frontend Chat UI:** Simple web-based interface built using HTML, CSS, and JavaScript.  
---

## 🔮 Future Improvements

- 🧩 **Add OAuth Authentication:** Secure admin access for managing escalation logs and chat analytics.  
- 🌍 **Multi-Language Support:** Extend AI responses to Hindi and other regional languages.  
- 📊 **Analytics Dashboard:** Track query types, response times, and customer satisfaction.  
- 🧠 **Fine-Tuned Model:** Train a domain-specific model using Razorpay FAQs for even higher accuracy.  
- ☁️ **Improved Deployment:** Move from Render to Railway or Dockerize for production reliability.  
