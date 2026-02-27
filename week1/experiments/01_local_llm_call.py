import requests

def chat(prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"]

if __name__ == "__main__":
    print(chat("Explain embeddings in 4 bullet points."))