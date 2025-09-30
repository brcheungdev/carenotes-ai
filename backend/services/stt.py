from __future__ import annotations

from io import BytesIO
from typing import Optional

from openai import OpenAI

from ..config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def transcribe_openai(file_bytes: bytes, filename: str, language: str = 'zh', model: Optional[str] = None) -> str:
    if not file_bytes:
        raise ValueError('invalid_audio')

    model_name = model or settings.OPENAI_TRANSCRIBE_MODEL
    try:
        response = client.audio.transcriptions.create(
            model=model_name,
            file=(filename, BytesIO(file_bytes)),
            response_format='text',
            language=language,
        )
    except Exception as exc:  # pragma: no cover - depends on SDK
        raise RuntimeError(f'transcribe_failed: {exc}') from exc

    text = getattr(response, 'text', None)
    if not text:
        raise RuntimeError('transcribe_failed: empty_response')
    return text.strip()
