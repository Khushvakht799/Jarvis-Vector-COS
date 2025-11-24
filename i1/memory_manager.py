# memory_manager.py
import sqlite3, json, os, uuid
from embedding_layer import EmbeddingLayer

class MemoryManager:
    def __init__(self, db_path="i1_memory.db", vec_dim=256):
        need_init = not os.path.exists(db_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.embed = EmbeddingLayer(model_name="all-MiniLM-L6-v2")  # пример названия модели

        if need_init:
            self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE memory (
                id TEXT PRIMARY KEY,
                type TEXT,
                text TEXT,
                vector TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                priority REAL DEFAULT 0.5
            )
        """)
        self.conn.commit()

    def store(self, type_, text, metadata=None, priority=0.5):
        mid = str(uuid.uuid4())
        vector = self.embed.encode_one(text)
        c = self.conn.cursor()
        c.execute("INSERT INTO memory (id,type,text,vector,metadata,priority) VALUES (?,?,?,?,?,?)",
                  (mid, type_, text, json.dumps(vector), json.dumps(metadata or {}), priority))
        self.conn.commit()
        return mid

    def query_similar(self, text, k=5):
        q = self.embed.encode_one(text)
        c = self.conn.cursor()
        rows = c.execute("SELECT id,type,text,vector,metadata,created_at,priority FROM memory").fetchall()
        scored = []
        for r in rows:
            vec = json.loads(r[3])
            score = sum(a*b for a,b in zip(q, vec))
            scored.append((score, r))
        scored.sort(key=lambda x: -x[0])
        return [ { "id": r[1][0] if False else r[1][0] } for _, r in scored[:k] ]
# --- Safe API for api_server -------------------------------------------------

_global_memory = MemoryManager(db_path="i1_demo_memory.db", vec_dim=256)

def save_to_memory(type_: str, text: str, metadata=None, priority: float = 0.5):
    """
    Safe wrapper used by api_server.
    Stores text into memory DB using global MemoryManager instance.
    """
    return _global_memory.store(type_, text, metadata, priority)


def load_from_memory(query_text: str, k: int = 5):
    """
    Safe wrapper used by api_server.
    Returns top-K similar memory entries.
    """
    return _global_memory.query_similar(query_text, k=k)
