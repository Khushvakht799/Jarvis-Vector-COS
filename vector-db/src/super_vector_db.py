import numpy as np
import pickle
import time

class SuperVectorDB:
    def __init__(self, dimensions=32000):
        self.dimensions = dimensions
        self.vectors = {}
        self.metadata = {}
        
    def add_vector(self, vector_id, vector, metadata=None):
        if len(vector) != self.dimensions:
            raise ValueError(f"Vector must be {self.dimensions}D")
        self.vectors[vector_id] = vector
        self.metadata[vector_id] = metadata or {}
        
    def similarity_search(self, query_vector, top_k=10):
        similarities = []
        for vec_id, vector in self.vectors.items():
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            similarities.append((vec_id, similarity, self.metadata[vec_id]))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
