import time
import pickle
import os

class MemorySnapshotSystem:
    def __init__(self, snapshot_dir="snapshots"):
        self.snapshot_dir = snapshot_dir
        self.snapshots = []
        os.makedirs(snapshot_dir, exist_ok=True)
        
    def create_snapshot(self, memory_state, description=""):
        snapshot_id = f"snapshot_{int(time.time())}"
        snapshot = {
            "id": snapshot_id,
            "timestamp": time.time(),
            "memory_state": memory_state,
            "description": description
        }
        filename = os.path.join(self.snapshot_dir, f"{snapshot_id}.pkl")
        with open(filename, "wb") as f:
            pickle.dump(snapshot, f)
        self.snapshots.append(snapshot)
        return snapshot_id
