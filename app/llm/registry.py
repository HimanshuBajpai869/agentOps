from app.llm.ollama_provider import OllamaProvider


class LLMRegistry:

    @staticmethod
    def get_provider(model_name="tinyllama"):
        return OllamaProvider(model=model_name)
