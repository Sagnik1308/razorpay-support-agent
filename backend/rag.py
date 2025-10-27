import os, json, faiss, numpy as np
from dotenv import load_dotenv
import requests

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
DOCS_PATH = os.path.join(DATA_DIR, "docs.jsonl")

_index, _docs = None, None

def load_index():
    global _index, _docs
    if _index is None:
        _index = faiss.read_index(INDEX_PATH)
        _docs = [json.loads(line) for line in open(DOCS_PATH)]
    return _index, _docs

def embed_query(text: str):
    r = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={"input": text, "model": os.getenv("EMBEDDING_MODEL")},
    )
    emb = np.array(r.json()["data"][0]["embedding"], dtype="float32")
    faiss.normalize_L2(emb.reshape(1, -1))
    return emb

def retrieve(query: str, top_k=5):
    index, docs = load_index()
    q = embed_query(query)
    scores, idxs = index.search(q.reshape(1, -1), top_k)
    results = []
    for score, idx in zip(scores[0], idxs[0]):
        d = docs[int(idx)]
        results.append({"text": d["text"], "url": d["url"], "score": float(score)})
    return results
