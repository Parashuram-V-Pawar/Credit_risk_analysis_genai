import faiss
import pickle
import numpy as np


class VectorStore:

    def __init__(self):
        self.index = None
        self.documents = []

    def build(self, embeddings, docs):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            embeddings.astype(np.float32)
        )

        self.documents = docs

    def search(self, embedding, k=3):

        embedding = np.array(
            embedding,
            dtype=np.float32
        )

        # Ensure shape = (1, dim)
        if len(embedding.shape) == 1:
            embedding = embedding.reshape(1, -1)

        distances, indices = self.index.search(
            embedding,
            k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):
                results.append(
                    self.documents[idx]
                )

        return results

    def save(self, path):

        faiss.write_index(
            self.index,
            f"{path}/index.faiss"
        )

        with open(
            f"{path}/documents.pkl",
            "wb"
        ) as f:

            pickle.dump(
                self.documents,
                f
            )

    def load(self, path):

        self.index = faiss.read_index(
            f"{path}/index.faiss"
        )

        with open(
            f"{path}/documents.pkl",
            "rb"
        ) as f:

            self.documents = pickle.load(f)