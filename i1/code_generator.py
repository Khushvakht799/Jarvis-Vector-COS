# code_generator.py
# Safe dynamic code generator for demonstration
from typing import List, Dict

def generate_code_for_plan(plan_steps: List[Dict]) -> List[Dict]:
    """
    Generates Python code snippets for each plan step.
    This is safe: only prints placeholders or simulated logic.
    """
    generated = []
    for step in plan_steps:
        step_type = step.get("type")
        payload = step.get("payload")

        # Safe placeholder logic
        if step_type == "analyze":
            code = f"# Analyze intent: {payload}\nprint('Analyzing {payload}')"
        elif step_type == "use_doc":
            code = f"# Consult documentation for: {payload}\nprint('Consulting {payload}')"
        elif step_type == "synthesize":
            code = f"# Synthesize result for: {payload}\nprint('Synthesizing {payload}')"
        else:
            code = f"# Step: {payload}\nprint('Executing {payload}')"

        generated.append({"step_id": step.get("step_id"), "code": code})

    return generated

# --- New: High-level code generator (required by api_server) ---
def generate_code(command: str, field: str) -> (str, Dict):
    """
    High-level wrapper used by api_server.
    Returns a tuple (code, meta) for MemoryManager integration.
    """
    # Meta может включать информацию о поле, команде, дате, и т.д.
    meta = {
        "field": field,
        "command": command,
        "description": f"Simulated execution of '{command}' on '{field}'"
    }

    # Safe placeholder code
    code = (
        f"# Jarvis execution plan\n"
        f"# Command: {command}\n"
        f"# Field: {field}\n\n"
        f"print('Executing command: {command} on field: {field}')\n"
    )

    return code, meta
