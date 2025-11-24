# api_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()

# Состояние Jarvis
state = {
    "last_field": None,
    "last_command": None,
    "use32kD": False
}

class CommandRequest(BaseModel):
    command: str
    field: str
    use32kD: bool

@app.post("/execute")
async def execute(cmd: CommandRequest):
    # Безболезненная инкриментация состояния
    state["last_field"] = cmd.field
    state["last_command"] = cmd.command
    state["use32kD"] = cmd.use32kD

    # Генерация результата
    result = f"Выполнена команда {cmd.command} на поле {cmd.field} (32kD={'ON' if cmd.use32kD else 'OFF'})"
    return {"result": result}
