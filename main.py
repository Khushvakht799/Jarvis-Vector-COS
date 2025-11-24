import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from vector_db.src.super_vector_db import SuperVectorDB, VectorFactory
from memory_snapshots.src.memory_system import SuperMemoryManager
from mig_engine.src.mig_engine import MIGEngine
from deepseek_integration.src.deepseek_integration import DeepSeekIntegration, CognitiveLoop

class JarvisCognitiveCore:
    """Ядро когнитивной ОС Jarvis"""
    
    def __init__(self):
        print("🚀 Инициализация Jarvis Cognitive OS...")
        
        # Инициализация компонентов
        self.vector_db = SuperVectorDB(dimensions=32000)
        self.memory_manager = SuperMemoryManager()
        self.mig_engine = MIGEngine()
        self.deepseek = DeepSeekIntegration()
        
        # Связывание компонентов
        self.memory_manager.connect_vector_db(self.vector_db)
        self.cognitive_loop = CognitiveLoop(self.vector_db, self.deepseek)
        
        print("✅ Jarvis Cognitive OS инициализирована")
    
    def process_input(self, text_input: str) -> dict:
        """Обработать текстовый ввод"""
        # МИГ-вычисления для быстрой обработки
        future = self.mig_engine.ephemeral_compute(
            f"process_{hash(text_input)}",
            self.cognitive_loop.process_query,
            text_input
        )
        
        result = future.result(timeout=10)
        
        # Создание снапшота памяти
        self.memory_manager.create_comprehensive_snapshot(
            f"Processing: {text_input[:30]}..."
        )
        
        return result
    
    def interactive_mode(self):
        """Интерактивный режим"""
        print("🤖 Jarvis Cognitive OS запущена в интерактивном режиме")
        print("Введите текст для обработки (или 'quit' для выхода)")
        
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                    
                if user_input:
                    result = self.process_input(user_input)
                    print(f"Ответ: {result['response_text']}")
                    print(f"Уверенность: {result['confidence']:.3f}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Ошибка: {e}")

if __name__ == "__main__":
    jarvis = JarvisCognitiveCore()
    jarvis.interactive_mode()
