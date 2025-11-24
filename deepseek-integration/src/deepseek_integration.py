import numpy as np
import os

class DeepSeekIntegration:
    def __init__(self, models_path=None):
        self.models_path = models_path or "C:/Users/usuario/Documents/1111/DeepSeak_models"
        self.vector_dimensions = 32000
        
    def text_to_vector(self, text):
        vector = np.zeros(self.vector_dimensions)
        for i, char in enumerate(text[:1000]):
            hash_val = (hash(char) + i) % self.vector_dimensions
            vector[hash_val] += 1.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector
