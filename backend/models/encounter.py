from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from sqlalchemy.sql import func

from ..db import db


def _isoformat(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=None).isoformat(timespec='seconds') + 'Z'
    return value.astimezone().isoformat(timespec='seconds')


class Encounter(db.Model):
    __tablename__ = 'encounters'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    admit_time = db.Column(db.DateTime)
    attending = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=func.now())

    patient = db.relationship('Patient', back_populates='encounters')
    notes = db.relationship('Note', back_populates='encounter')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id) if self.id is not None else None,
            'patient_id': str(self.patient_id) if self.patient_id is not None else None,
            'admit_time': _isoformat(self.admit_time),
            'attending': self.attending,
        }

    def __repr__(self) -> str:  # pragma: no cover - repr utility
        return f'<Encounter id={self.id} patient_id={self.patient_id}>'
