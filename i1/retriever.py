# retriever.py
from embedding_layer import EmbeddingLayer

class Retriever:
    def __init__(self):
        self.embed_layer = EmbeddingLayer()

    def add_knowledge(self, text, meta):
        self.embed_layer.add(text, meta)

    def retrieve(self, query, top_k=3):
        return self.embed_layer.search(query, top_k)
