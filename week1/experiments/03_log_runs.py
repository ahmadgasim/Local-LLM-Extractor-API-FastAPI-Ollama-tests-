import json
from datetime import datetime
from llm_client import OllamaLLM

llm = OllamaLLM(model="llama3.1:8b")

prompt = "Explain embeddings in 4 bullets. Add one real example."
out = llm.generate(prompt, temperature=0.2)

record = {
    "ts": datetime.utcnow().isoformat() + "Z",
    "model": llm.model,
    "temperature": 0.2,
    "prompt": prompt,
    "output": out,
}

with open(r"week1/experiments/runs.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(out)
print("\nSaved to week1/experiments/runs.jsonl")