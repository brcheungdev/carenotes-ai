from __future__ import annotations

import json
from typing import Any, Dict

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

from ..config import settings


SYSTEM_PROMPT = (
    '你是护理记录抽取助手。仅输出 JSON（无任何多余字符），结构如下：\n'
    '{  "vitals":{"temp":浮点或null,"hr":整型或null,"rr":整型或null,"bp_sys":整型或null,"bp_dia":整型或null,"spo2":整型或null},\n'
    '  "pain_score":0-10或null,\n'
    '  "intake_ml":整型或null,\n'
    '  "output_ml":整型或null,\n'
    '  "subjective":"字符串",\n'
    '  "objective":"字符串",\n'
    '  "assessment":"字符串",\n'
    '  "plan":"字符串",\n'
    '  "med_given":[{"name":"药名","dose":"剂量","route":"途径","time":"ISO8601"}],\n'
    '  "alerts":[字符串\n]}\n'
    '规则：不得编造；未提及填null；中文口语数词需转数字（“九十七”→97）。'
)

_client = OpenAI(api_key=settings.OPENAI_API_KEY)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _invoke_llm(text: str, model_override: str | None = None) -> str:
    model_name = model_override or settings.OPENAI_PARSE_MODEL
    response = _client.responses.create(
        model=model_name,
        messages=[
            {
                'role': 'system',
                'content': [{'type': 'text', 'text': SYSTEM_PROMPT}],
            },
            {
                'role': 'user',
                'content': [{'type': 'text', 'text': text}],
            },
        ],
        response_format={'type': 'json_object'},
    )
    try:
        message = response.output[0]
        content = message.content[0].text
    except (AttributeError, IndexError, KeyError) as exc:  # pragma: no cover - defensive
        raise RuntimeError('llm_invalid_response') from exc
    return content


def parse_note(text: str) -> Dict[str, Any]:
    try:
        raw = _invoke_llm(text)
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError('llm_parse_failed_json') from exc
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc

    return data


__all__ = ['parse_note', 'SYSTEM_PROMPT']
