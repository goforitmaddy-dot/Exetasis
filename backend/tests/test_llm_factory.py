import pytest
from backend.app.core.config import settings
from backend.app.services.llm.client import MockLLMClient, VLLMClient
from backend.app.services.llm.factory import get_llm_client


def test_llm_factory_mock():
    """Verify factory returns MockLLMClient when configured."""
    settings.LLM_PROVIDER = "mock"
    client = get_llm_client()
    assert isinstance(client, MockLLMClient)


def test_llm_factory_vllm():
    """Verify factory returns VLLMClient when configured."""
    settings.LLM_PROVIDER = "vllm"
    client = get_llm_client()
    assert isinstance(client, VLLMClient)


def test_llm_factory_gemini_disabled_by_default():
    """Verify Gemini cannot be used when GEMINI_ENABLED is False (Rule 9)."""
    settings.LLM_PROVIDER = "gemini"
    settings.GEMINI_ENABLED = False
    client = get_llm_client()
    # Should safely fallback to Mock client
    assert isinstance(client, MockLLMClient)
