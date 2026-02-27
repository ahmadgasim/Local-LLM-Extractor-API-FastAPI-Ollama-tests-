import time
from typing import Optional

import requests

OLLAMA_URL = "http://localhost:11434"


class OllamaLLM:
    def __init__(self, model: str = "llama3.1:8b", base_url: str = OLLAMA_URL, timeout: int = 120):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, *, temperature: Optional[float] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        if temperature is not None:
            payload["options"] = {"temperature": temperature}

        last_error: Exception | None = None

        for attempt in range(3):
            try:
                r = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=self.timeout,
                )
                r.raise_for_status()

                data = r.json()
                text = data.get("response")
                if not isinstance(text, str):
                    raise RuntimeError(f"Unexpected response format: {data}")

                return text

            except Exception as e:
                last_error = e
                # simple backoff: 1s, 2s, 3s
                time.sleep(1.0 * (attempt + 1))

        raise RuntimeError(f"LLM request failed after 3 attempts: {last_error}")