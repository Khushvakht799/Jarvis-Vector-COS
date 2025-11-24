# brain_service/src/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json
from typing import List, Dict, Any

app = FastAPI(title="Jarvis Brain Service")

# CORS для коммуникации с Go сервисом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BrainRequest(BaseModel):
    prompt: str
    context: Dict[str, Any] = {}
    session_id: str = "default"

class BrainResponse(BaseModel):
    answer: str
    reasoning: str
    actions: List[str]
    confidence: float
    memory_used: bool
    processed_by: str = "Python Brain"

class VectorMemory:
    def __init__(self):
        self.memory_vectors = []
        self.memory_texts = []
        # Простой эмбеддинг через усреднение слов (позже заменим на sentence-transformers)
    
    def simple_embedding(self, text: str) -> List[float]:
        """Простой эмбеддинг для демонстрации"""
        words = text.lower().split()
        vector = [len(word) for word in words]  # Примитивный эмбеддинг
        # Нормализация
        if vector:
            max_val = max(vector)
            vector = [v/max_val for v in vector]
        return vector + [0] * (10 - len(vector))  # Дополнение до 10 измерений
    
    def store(self, text: str):
        vector = self.simple_embedding(text)
        self.memory_vectors.append(vector)
        self.memory_texts.append(text)
    
    def search(self, query: str, top_k: int = 2) -> List[str]:
        if not self.memory_vectors:
            return []
        
        query_vector = self.simple_embedding(query)
        # Простая схожесть через евклидово расстояние
        similarities = []
        for memory_vec in self.memory_vectors:
            dist = np.linalg.norm(np.array(memory_vec) - np.array(query_vector))
            similarities.append(1 / (1 + dist))  # Конвертируем расстояние в схожесть
        
        indices = np.argsort(similarities)[-top_k:]
        return [self.memory_texts[i] for i in indices if similarities[i] > 0.3]

# Инициализация памяти
memory = VectorMemory()

@app.post("/process", response_model=BrainResponse)
async def process_brain(request: BrainRequest):
    print(f"🧠 Brain received: {request.prompt}")
    
    # Сохраняем в память
    memory.store(request.prompt)
    
    # Ищем релевантные воспоминания
    relevant_memories = memory.search(request.prompt)
    memory_used = len(relevant_memories) > 0
    
    # Базовая когнитивная обработка
    reasoning = "Когнитивный анализ с контекстуальным пониманием"
    if memory_used:
        reasoning += f". Использована память: {relevant_memories}"
    
    response = BrainResponse(
        answer=f"🧠 Обработано мозгом: '{request.prompt}'. Память: {len(memory.memory_texts)} записей",
        reasoning=reasoning,
        actions=["cognitive_processing", "memory_store", "context_analysis"],
        confidence=0.92,
        memory_used=memory_used
    )
    
    return response

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Jarvis Brain",
        "memory_size": len(memory.memory_texts)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)