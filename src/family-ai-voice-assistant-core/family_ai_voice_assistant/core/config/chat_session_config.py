from dataclasses import dataclass
from .config import Config


@dataclass
class ChatSessionConfig(Config):
    init_prompt_path: str = None
    max_token_per_session: int = -1
    session_timeout: int = 300
