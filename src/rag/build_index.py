from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore
from src.rag.document_loader import load_documents

docs = []

docs.extend(
    load_documents("data/policies")
)

docs.extend(
    load_documents("data/historical_cases")
)

embedder = Embedder()

embeddings = embedder.encode(docs)

store = VectorStore()

store.build(
    embeddings,
    docs
)

store.save("src/rag/index")

print("RAG Index Built")