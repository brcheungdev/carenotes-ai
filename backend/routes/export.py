from __future__ import annotations

from io import BytesIO

from flask import Blueprint, send_file

from ..models import Note, Patient
from ..services import generate_note_pdf
from . import NotFoundError, token_required


export_bp = Blueprint('export', __name__)


@export_bp.get('/notes/<int:note_id>')
@token_required()
def export_note(note_id: int):
    note = Note.query.get(note_id)
    if not note:
        raise NotFoundError('note_not_found')
    patient = Patient.query.get(note.patient_id)
    if not patient:
        raise NotFoundError('patient_not_found')

    pdf_bytes = generate_note_pdf(note, patient=patient)
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'note_{note_id}.pdf',
    )
