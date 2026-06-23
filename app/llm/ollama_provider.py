import requests
from app.llm.base import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(self, model: str = "tinyllama"):
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "stream": False,
            },
        )

        return response.json()["response"]
