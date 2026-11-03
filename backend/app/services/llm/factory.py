from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.services.llm.client import (
    GeminiClient,
    LLMClient,
    MockLLMClient,
    OllamaClient,
    VLLMClient,
)


def get_llm_client() -> LLMClient:
    """Factory creating an LLM client instance based on environment settings.

    Only open-source local providers (Ollama / vLLM) or Mock client are permitted by default.
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "ollama":
        logger.info("Initializing Ollama client (%s at %s)", settings.OLLAMA_MODEL, settings.OLLAMA_BASE_URL)
        return OllamaClient()

    elif provider == "vllm":
        logger.info("Initializing vLLM client (%s at %s)", settings.VLLM_MODEL, settings.VLLM_BASE_URL)
        return VLLMClient()

    elif provider == "mock":
        logger.info("Initializing MockLLMClient for testing")
        return MockLLMClient()

    elif provider == "gemini":
        if not settings.GEMINI_ENABLED:
            logger.warning("Gemini requested but GEMINI_ENABLED=false. Falling back to MockLLMClient.")
            return MockLLMClient()
        return GeminiClient()

    logger.warning("Unknown LLM_PROVIDER '%s'. Falling back to MockLLMClient.", provider)
    return MockLLMClient()
