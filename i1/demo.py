# demo.py — simplified generated code for safe increment
import json
from flask import Flask, request

app = Flask(__name__)

# Dummy mapping of plan steps → generated code snippets
step_to_code = {
    "deploy": "print('Deploying application...')",
    "db_update": "print('Updating database...')",
}

@app.route("/i1/submit", methods=["POST"])
def submit():
    data = request.json
    text = data.get("text", "")

    # Simple plan: just split words and assign dummy types
    plan_steps = []
    for word in text.lower().split():
        if word in step_to_code:
            plan_steps.append({"payload": word, "type": "retrieved"})

    # Generated code for each plan step
    generated = []
    for step in plan_steps:
        generated.append({
            "step_id": step["payload"],
            "code": step_to_code.get(step["payload"], "# pass")
        })

    response = {
        "status": "ok",
        "plan": plan_steps,
        "generated": {"generated": generated}
    }
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001)
