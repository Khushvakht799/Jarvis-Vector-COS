from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class EmbeddingLayer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Load SBERT model
        self.model = SentenceTransformer(model_name)
        self.vectors = []
        self.metadata = []
        self.index = None

    def add(self, text, meta):
        vec = self.model.encode([text])[0].astype('float32')
        self.vectors.append(vec)
        self.metadata.append(meta)
        self._rebuild_index()

    def _rebuild_index(self):
        if self.vectors:
            self.index = faiss.IndexFlatL2(len(self.vectors[0]))
            self.index.add(np.array(self.vectors))

    def search(self, query, top_k=3):
        if not self.index:
            return []
        q_vec = self.model.encode([query])[0].astype('float32')
        D, I = self.index.search(np.array([q_vec]), top_k)
        results = [self.metadata[i] for i in I[0]]
        return results
