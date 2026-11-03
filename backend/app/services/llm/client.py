from abc import ABC, abstractmethod
from typing import Optional
import httpx
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from backend.app.core.config import settings
from backend.app.core.logging import logger


class LLMClient(ABC):
    """Abstract interface for local open-source LLM runners."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response text from the LLM."""
        pass


class MockLLMClient(LLMClient):
    """STUB: Mock LLM client returning deterministic stubbed responses for testing."""

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        logger.debug("[STUB] MockLLMClient generate called with prompt length %d", len(prompt))
        return "STUB: Mock LLM response evaluating workplace signals."


class OllamaClient(LLMClient):
    """Client for locally served open-source models via Ollama."""

    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL, model: str = settings.OLLAMA_MODEL) -> None:
        self.base_url = base_url
        self.model = model
        self._llm = ChatOllama(base_url=self.base_url, model=self.model)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        response = await self._llm.ainvoke(messages)
        return str(response.content)


class VLLMClient(LLMClient):
    """Client for local or AMD-hosted vLLM using async HTTP REST without proprietary SDKs."""

    def __init__(self, base_url: str = settings.VLLM_BASE_URL, model: str = settings.VLLM_MODEL) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.warning("vLLM connection failed, returning fallback STUB: %s", e)
                return f"STUB: vLLM evaluation output (model={self.model})"


class GeminiClient(LLMClient):
    """Optional Gemini client: disabled by default per Rule 9."""

    def __init__(self) -> None:
        if not settings.GEMINI_ENABLED:
            raise RuntimeError("Gemini provider is disabled by default. Enable GEMINI_ENABLED=true in .env to use.")

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        # STUB: Optional provider implementation
        return "STUB: Gemini response (optional provider)"
