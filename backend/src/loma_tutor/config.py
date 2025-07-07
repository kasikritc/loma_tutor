from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    # --- Groq Configuration ---
    GROQ_API_KEY: str = ""
    GROQ_LLM_MODEL: str = "meta-llama/llama-4-maverick-17b-128e-instruct"
    GROQ_LLM_TEMPERATURE: float = 0.7

    # --- OpenAI Configuration ---
    OPENAI_API_KEY: str = ""
    OPENAI_LLM_MODEL: str = "gpt-4.1"
    OPENAI_LLM_TEMPERATURE: float = 0.7

    # --- MongoDB Configuration ---
    MONGO_URI: str = Field(
        default="mongodb://philoagents:philoagents@local_dev_atlas:27017/?directConnection=true",
        description="Connection URI for the local MongoDB Atlas instance.",
    )
    MONGO_DB_NAME: str = "philoagents"
    MONGO_STATE_CHECKPOINT_COLLECTION: str = "philosopher_state_checkpoints"
    MONGO_STATE_WRITES_COLLECTION: str = "philosopher_state_writes"
    MONGO_LONG_TERM_MEMORY_COLLECTION: str = "philosopher_long_term_memory"

    # --- Agents Configuration ---
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 30
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5
    
    # --- Agent's LLM Configuration ---
    QA_GENERATOR_LLM_PROVIDER: str = "Groq"
    TUTOR_LLM_PROVIDER: str = "Groq"

settings = Settings()
