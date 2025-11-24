import time
from concurrent.futures import ThreadPoolExecutor

class MIGEngine:
    def __init__(self):
        self.ephemeral_tasks = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        
    def ephemeral_compute(self, task_id, function, *args, ttl=5.0):
        def task_wrapper():
            try:
                result = function(*args)
                self.ephemeral_tasks[task_id] = {
                    "result": result,
                    "created": time.time(),
                    "ttl": ttl
                }
                return result
            except Exception as e:
                print(f"Task {task_id} failed: {e}")
        return self.executor.submit(task_wrapper)
