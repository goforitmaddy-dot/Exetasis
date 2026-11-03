from typing import List, Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General App Config
    APP_NAME: str = "Exetasis"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./exetasis.db"

    # LLM Settings (Open-source / local models only)
    LLM_PROVIDER: Literal["ollama", "vllm", "mock"] = "ollama"

    # Ollama settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:latest"

    # Provisional MVP weights: equal weight is a transparent starting convention, not a validated HR measure.
    CONTRIBUTION_DIMENSION_WEIGHTS: dict[str, float] = Field(default_factory=lambda: {
        "task_completion": 1.0,
        "difficulty": 1.0,
        "quality": 1.0,
        "review_acceptance": 1.0,
        "rework": 1.0,
        "mentoring_unblocking": 1.0,
    })

    @field_validator("CONTRIBUTION_DIMENSION_WEIGHTS")
    @classmethod
    def validate_contribution_weights(cls, value: dict[str, float]) -> dict[str, float]:
        expected = {"task_completion", "difficulty", "quality", "review_acceptance", "rework", "mentoring_unblocking"}
        if set(value) != expected or any(weight <= 0 for weight in value.values()):
            raise ValueError(f"Contribution weights must provide positive values for exactly: {sorted(expected)}")
        return value

    # vLLM settings (Local or AMD-hosted)
    VLLM_BASE_URL: str = "http://localhost:8000/v1"
    VLLM_MODEL: str = "meta-llama/Llama-3.2-3B-Instruct"

    # Optional Gemini settings (Strictly disabled by default)
    GEMINI_ENABLED: bool = False
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # WebSocket
    WS_HEARTBEAT_INTERVAL_SECONDS: int = 15


settings = Settings()
