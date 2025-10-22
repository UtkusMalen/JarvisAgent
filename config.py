import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Application config"""

    api_key: str
    model_name: str = "gemini-flash-latest"
    system_instruction: str = (
        "You are Jarvis, a helpful desktop assistant for Kubuntu Linux"
        "Your job is to interpret user commands and call the appropriate system functions"
        "Always respond concisely and confirm what action you're taking"
        "Available system: Kubuntu (KDE Plasma desktop environment)"
    )
    command_timeout: int = 10

    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from env vars"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY env var is not set"
            )
        return cls(api_key=api_key)