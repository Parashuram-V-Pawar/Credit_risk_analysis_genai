from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore


class RAGEngine:

    def __init__(self):

        self.embedder = Embedder()

        self.store = VectorStore()

        self.store.load(
            "src/rag/index"
        )

    def retrieve(self, query):

        embedding = self.embedder.encode(
            [query]
        )

        return self.store.search(
            embedding
        )