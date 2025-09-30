# backend/config.py
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR  = Path(__file__).resolve().parent
ENV_PATH  = BASE_DIR / ".env"

# �ؼ�����ʽ·�� + override=True���ѿ�/��ֵ���ǵ���
load_dotenv(dotenv_path=str(ENV_PATH), override=True)

def _get(key: str, default: str | None = None) -> str | None:
    v = os.getenv(key)
    return v if v not in ("", None) else default

@dataclass(slots=True)
class Settings:
    mysql_url: str
    openai_api_key: str | None
    openai_transcribe_model: str
    openai_parse_model: str
    jwt_secret: str

    @property
    def MYSQL_URL(self) -> str: return self.mysql_url
    @property
    def OPENAI_API_KEY(self) -> str | None: return self.openai_api_key
    @property
    def OPENAI_TRANSCRIBE_MODEL(self) -> str: return self.openai_transcribe_model
    @property
    def OPENAI_PARSE_MODEL(self) -> str: return self.openai_parse_model
    @property
    def JWT_SECRET(self) -> str: return self.jwt_secret

settings = Settings(
    mysql_url=_get("MYSQL_URL", "mysql+pymysql://mysql用户名:mysql密码@localhost:3306/carenotes"),
    openai_api_key=_get("OPENAI_API_KEY", "你的apikey"),
    openai_transcribe_model=_get("OPENAI_TRANSCRIBE_MODEL", "whisper-1"),
    openai_parse_model=_get("OPENAI_PARSE_MODEL", "gpt-4o-mini"),
    jwt_secret=_get("JWT_SECRET", "dev_secret"),
)
