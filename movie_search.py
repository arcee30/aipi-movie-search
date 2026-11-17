from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DATABASE_PATH = PROJECT_DIR / "chromadb"


def load_model():
    try:
        return SentenceTransformer(MODEL_NAME, local_files_only=True)
    except OSError:
        return SentenceTransformer(MODEL_NAME)


def collection_name(movie_limit):
    suffix = "all" if movie_limit is None else str(movie_limit)
    return f"movie_plots_{suffix}"


def semantic_search(query, model, collection):
    vector = model.encode([query])
    result = collection.query(query_embeddings=vector, n_results=1)
    return result["metadatas"][0][0], result["documents"][0][0]


def database():
    return chromadb.PersistentClient(path=str(DATABASE_PATH))
