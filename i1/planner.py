# planner.py
import uuid

class Planner:
    def plan(self, intent: str, context_docs: list):
        plan_id = str(uuid.uuid4())
        steps = []
        steps.append({"step_id": "s1", "type": "analyze", "payload": intent})
        for i, d in enumerate(context_docs[:3]):
            steps.append({"step_id": f"s{i+2}", "type": "use_doc", "payload": d.get("id", "doc")})
        steps.append({"step_id": "s_end", "type": "synthesize", "payload": "generate_solution"})
        return {"plan_id": plan_id, "steps": steps, "estimated_risk": 0.2}
