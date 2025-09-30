from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.sql import func

from ..db import db


def _isoformat(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=None).isoformat(timespec='seconds') + 'Z'
    return value.astimezone().isoformat(timespec='seconds')


def _load_json(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return value


def _dump_json(value: Any) -> Any:
    if value in (None, ''):
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return value


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounters.id'))
    created_at = db.Column(db.DateTime, server_default=func.now())
    vitals = db.Column(db.JSON)
    pain_score = db.Column(db.Integer)
    intake_ml = db.Column(db.Integer)
    output_ml = db.Column(db.Integer)
    subjective = db.Column(db.Text)
    objective = db.Column(db.Text)
    assessment = db.Column(db.Text)
    plan = db.Column(db.Text)
    med_given = db.Column(db.JSON)
    alerts = db.Column(db.JSON)
    signed = db.Column(db.Integer, default=0)
    transcript = db.Column(db.Text)

    patient = db.relationship('Patient', back_populates='notes')
    encounter = db.relationship('Encounter', back_populates='notes')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id) if self.id is not None else None,
            'patient_id': str(self.patient_id) if self.patient_id is not None else None,
            'encounter_id': str(self.encounter_id) if self.encounter_id is not None else None,
            'created_at': _isoformat(self.created_at),
            'vitals': _load_json(self.vitals) or {
                'temp': None,
                'hr': None,
                'rr': None,
                'bp_sys': None,
                'bp_dia': None,
                'spo2': None,
            },
            'pain_score': self.pain_score,
            'intake_ml': self.intake_ml,
            'output_ml': self.output_ml,
            'subjective': self.subjective,
            'objective': self.objective,
            'assessment': self.assessment,
            'plan': self.plan,
            'med_given': _load_json(self.med_given) or [],
            'alerts': _load_json(self.alerts) or [],
            'signed': bool(self.signed),
            'transcript': self.transcript,
        }

    def set_json_fields(self, *, vitals: Optional[Any] = None, med_given: Optional[Any] = None, alerts: Optional[Any] = None) -> None:
        if vitals is not None:
            self.vitals = _dump_json(vitals)
        if med_given is not None:
            self.med_given = _dump_json(med_given)
        if alerts is not None:
            self.alerts = _dump_json(alerts)

    def __repr__(self) -> str:  # pragma: no cover - repr utility
        return f'<Note id={self.id} patient_id={self.patient_id}>'
