# nlp_utils.py
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np
import nltk
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

# Embedding model name
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Ensure NLTK data available (only punkt required)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    try:
        nltk.download("punkt", quiet=True)
    except Exception as e:
        logger.warning("NLTK punkt download failed: %s", e)

@lru_cache(maxsize=1)
def _embedder():
    try:
        return SentenceTransformer(EMBEDDING_MODEL)
    except Exception as e:
        logger.error("Failed to load embedding model %s: %s", EMBEDDING_MODEL, e)
        raise

def embed_texts(texts, convert_to_tensor=True):
    return _embedder().encode(texts, convert_to_tensor=convert_to_tensor)

def rank_papers_by_query(query: str, papers: list, top_k: int = 6) -> list:
    abstracts = [p.get("abstract", "") or "" for p in papers]
    if not abstracts:
        return []
    model = _embedder()
    query_emb = model.encode(query, convert_to_tensor=True)
    abs_embs = model.encode(abstracts, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, abs_embs)[0].cpu().numpy()
    idx = np.argsort(-scores)[:top_k]
    ranked = []
    for i in idx:
        p = papers[i].copy()
        p["score"] = float(scores[i])
        ranked.append(p)
    return ranked

def split_sentences(text: str):
    from nltk.tokenize import sent_tokenize
    if not text:
        return []
    return sent_tokenize(text)

def extractive_summary_by_embedding(text: str, top_n: int = 2) -> str:
    sents = split_sentences(text)
    if not sents:
        return ""
    model = _embedder()
    sent_embs = model.encode(sents, convert_to_tensor=True)
    doc_emb = model.encode(text, convert_to_tensor=True)
    scores = util.cos_sim(doc_emb, sent_embs)[0].cpu().numpy()
    best_idx = list(np.argsort(-scores)[:top_n])
    selected = [sents[i] for i in sorted(best_idx)]
    return " ".join(selected)
