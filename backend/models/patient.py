from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict

from sqlalchemy.sql import func

from ..db import db


def _isoformat(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=None).isoformat(timespec='seconds') + 'Z'
    return value.astimezone().isoformat(timespec='seconds')


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    mrn = db.Column(db.String(64))
    ward = db.Column(db.String(64))
    bed = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, server_default=func.now())

    encounters = db.relationship('Encounter', back_populates='patient', cascade='all, delete-orphan')
    notes = db.relationship('Note', back_populates='patient', cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, Any]:
        dob_value = self.dob.isoformat() if isinstance(self.dob, date) else None
        return {
            'id': str(self.id) if self.id is not None else None,
            'name': self.name,
            'gender': self.gender,
            'dob': dob_value,
            'mrn': self.mrn,
            'ward': self.ward,
            'bed': self.bed,
            'created_at': _isoformat(self.created_at),
        }

    def __repr__(self) -> str:  # pragma: no cover - repr utility
        return f'<Patient id={self.id} name={self.name!r}>'
