# from llm_client import OllamaLLM
from week1.experiments.llm_client import OllamaLLM

llm = OllamaLLM(model="llama3.1:8b")

prompt = "Give 4 bullet points explaining embeddings. Keep it concise."

for t in [0.0, 0.3, 0.9]:
    print(f"\n--- temperature={t} ---")
    print(llm.generate(prompt, temperature=t))