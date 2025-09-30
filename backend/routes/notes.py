from __future__ import annotations

from typing import Any, Dict

from flask import Blueprint, g, request

from ..db import db
from ..models import AuditEvent, Note, Patient
from ..services import detect_alerts, parse_note, transcribe_openai
from . import APIError, NotFoundError, UnprocessableError, success_response, token_required


notes_bp = Blueprint('notes', __name__)


@notes_bp.post('/transcribe')
@token_required()
def transcribe():
    if 'file' not in request.files:
        raise APIError('file_required', code='bad_request', status_code=400)
    uploaded = request.files['file']
    file_bytes = uploaded.read()
    filename = uploaded.filename or 'audio.webm'
    try:
        text = transcribe_openai(file_bytes, filename)
    except ValueError as exc:
        raise APIError(str(exc), code='bad_request', status_code=400) from exc
    except RuntimeError as exc:
        raise APIError(str(exc), code='server_error', status_code=500) from exc

    return success_response({'text': text})


@notes_bp.post('/parse')
@token_required()
def parse():
    payload = request.get_json(silent=True) or {}
    text = (payload.get('text') or '').strip()
    if not text:
        raise APIError('text_required', code='bad_request', status_code=400)

    try:
        parsed = parse_note(text)
    except RuntimeError as exc:
        raise UnprocessableError('parse_failed') from exc

    vitals = parsed.get('vitals') or {}
    alerts = parsed.get('alerts') or []
    rule_alerts = detect_alerts(vitals)
    merged_alerts = []
    seen = set()
    for item in [*alerts, *rule_alerts]:
        if item and item not in seen:
            merged_alerts.append(item)
            seen.add(item)
    parsed['alerts'] = merged_alerts

    return success_response(parsed)


def _coerce_int(value: Any) -> int | None:
    if value in (None, '', 'null'):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise APIError('invalid_integer', code='bad_request', status_code=400)


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {'1', 'true', 'yes'}
    return bool(value)


@notes_bp.post('')
@token_required()
def create_note():
    payload: Dict[str, Any] = request.get_json(silent=True) or {}
    patient_id = _coerce_int(payload.get('patient_id'))
    if not patient_id:
        raise APIError('patient_id_required', code='bad_request', status_code=400)

    patient = Patient.query.get(patient_id)
    if not patient:
        raise NotFoundError('patient_not_found')

    encounter_id = _coerce_int(payload.get('encounter_id'))

    note = Note(
        patient_id=patient_id,
        encounter_id=encounter_id,
        pain_score=_coerce_int(payload.get('pain_score')),
        intake_ml=_coerce_int(payload.get('intake_ml')),
        output_ml=_coerce_int(payload.get('output_ml')),
        subjective=payload.get('subjective'),
        objective=payload.get('objective'),
        assessment=payload.get('assessment'),
        plan=payload.get('plan'),
        signed=1 if _coerce_bool(payload.get('signed')) else 0,
        transcript=payload.get('transcript'),
    )
    note.set_json_fields(
        vitals=payload.get('vitals'),
        med_given=payload.get('med_given'),
        alerts=payload.get('alerts'),
    )

    db.session.add(note)
    db.session.commit()

    audit = AuditEvent(
        user=getattr(g, 'current_user', None).username if hasattr(g, 'current_user') else None,
        action='create',
        entity='note',
        entity_id=note.id,
    )
    audit.set_diff(payload)
    db.session.add(audit)
    db.session.commit()

    return success_response(note.to_dict(), status_code=201)


@notes_bp.get('/<int:note_id>')
@token_required()
def get_note(note_id: int):
    note = Note.query.get(note_id)
    if not note:
        raise NotFoundError('note_not_found')
    return success_response(note.to_dict())


