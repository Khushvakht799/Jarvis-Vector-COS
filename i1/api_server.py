from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from code_generator import generate_code
from memory_manager import MemoryManager

# Один экземпляр FastAPI
app = FastAPI()

# CORS для GUI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Память
memory = MemoryManager(db_path="i1_memory.db", vec_dim=256)

# Модель запроса
class CommandRequest(BaseModel):
    command: str
    field: str

# Маршрут /execute
@app.post("/execute")
async def execute_command(req: CommandRequest):
    try:
        # Генерация кода
        code, meta = generate_code(req.command, req.field)
        # Сохраняем в память
        memory.store(req.field, code, metadata=meta)
        # Возвращаем первые 200 символов + метаданные
        return {"status": "ok", "output": code[:200] + "...", "meta": meta}
    except Exception as e:
        return {"status": "error", "message": str(e)}
