import os, requests, json, faiss, numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
URL_LIST = os.path.join(DATA_DIR, "seed_urls.txt")
DOCS_PATH = os.path.join(DATA_DIR, "docs.jsonl")
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())
    return text

def embed_batch(texts):
    r = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json",
        },
        json={"input": texts, "model": EMBED_MODEL},
    )
    data = r.json()["data"]
    return [d["embedding"] for d in data]

def crawl_and_split():
    docs = []
    with open(URL_LIST) as f:
        urls = [u.strip() for u in f if u.strip()]
    for url in tqdm(urls, desc="Fetching docs"):
        try:
            html = requests.get(url, timeout=10).text
            text = clean_text(html)
            # split into ~700-char chunks
            for i in range(0, len(text), 700):
                chunk = text[i : i + 700]
                docs.append({"url": url, "text": chunk})
        except Exception as e:
            print("Error fetching", url, e)
    return docs

def build_index():
    docs = crawl_and_split()
    with open(DOCS_PATH, "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")

    print(f"Embedding {len(docs)} chunks...")
    embs = []
    for i in tqdm(range(0, len(docs), 50), desc="Embedding"):
        batch = [d["text"] for d in docs[i : i + 50]]
        batch_embs = embed_batch(batch)
        embs.extend(batch_embs)

    arr = np.array(embs).astype("float32")
    faiss.normalize_L2(arr)
    index = faiss.IndexFlatIP(arr.shape[1])
    index.add(arr)
    faiss.write_index(index, INDEX_PATH)
    print(f"✅ Index built → {INDEX_PATH}  |  Docs → {DOCS_PATH}")

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    build_index()
