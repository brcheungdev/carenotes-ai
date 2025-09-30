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


class AuditEvent(db.Model):
    __tablename__ = 'audit_events'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    action = db.Column(db.String(64))
    entity = db.Column(db.String(64))
    entity_id = db.Column(db.Integer)
    at = db.Column(db.DateTime, server_default=func.now())
    diff_json = db.Column(db.JSON)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id) if self.id is not None else None,
            'user': self.user,
            'action': self.action,
            'entity': self.entity,
            'entity_id': str(self.entity_id) if self.entity_id is not None else None,
            'at': _isoformat(self.at),
            'diff_json': _load_json(self.diff_json),
        }

    def set_diff(self, value: Optional[Any]) -> None:
        self.diff_json = _dump_json(value)

    def __repr__(self) -> str:  # pragma: no cover
        return f'<AuditEvent id={self.id} entity={self.entity}>'
