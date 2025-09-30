from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from flask import Blueprint, request

from ..db import db
from ..models import Note, Patient
from . import APIError, NotFoundError, success_response, token_required


patients_bp = Blueprint('patients', __name__)


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace('Z', '+00:00')
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise APIError(f'invalid_date: {value}', code='bad_request', status_code=400) from exc


@patients_bp.post('')
@token_required()
def create_patient():
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    if not name:
        raise APIError('name_required', code='bad_request', status_code=400)

    dob_value = payload.get('dob')
    dob = _parse_datetime(dob_value).date() if dob_value else None

    patient = Patient(
        name=name,
        gender=payload.get('gender'),
        dob=dob,
        mrn=payload.get('mrn'),
        ward=payload.get('ward'),
        bed=payload.get('bed'),
    )
    db.session.add(patient)
    db.session.commit()
    return success_response(patient.to_dict(), status_code=201)


@patients_bp.get('/<int:patient_id>')
@token_required()
def get_patient(patient_id: int):
    patient = Patient.query.get(patient_id)
    if not patient:
        raise NotFoundError('patient_not_found')
    return success_response(patient.to_dict())


@patients_bp.get('/<int:patient_id>/notes')
@token_required()
def list_patient_notes(patient_id: int):
    patient = Patient.query.get(patient_id)
    if not patient:
        raise NotFoundError('patient_not_found')

    query = Note.query.filter_by(patient_id=patient_id).order_by(Note.created_at.desc())

    from_param = request.args.get('from')
    to_param = request.args.get('to')
    alerts_only = request.args.get('alerts_only') in {'1', 'true', 'True'}
    signed_only = request.args.get('signed_only') in {'1', 'true', 'True'}

    if from_param:
        from_dt = _parse_datetime(from_param)
        if from_dt:
            query = query.filter(Note.created_at >= from_dt)
    if to_param:
        to_dt = _parse_datetime(to_param)
        if to_dt:
            query = query.filter(Note.created_at <= to_dt)

    notes: List[Dict[str, Any]] = []
    for note in query:
        note_dict = note.to_dict()
        if alerts_only and not note_dict.get('alerts'):
            continue
        if signed_only and not note_dict.get('signed'):
            continue
        notes.append(note_dict)

    meta = {'count': len(notes)}
    data = {
        'patient': patient.to_dict(),
        'notes': notes,
    }
    return success_response(data, meta=meta)
