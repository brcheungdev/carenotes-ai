from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader, select_autoescape

try:  # Prefer HTML -> PDF rendering when available
    from weasyprint import HTML  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    HTML = None  # type: ignore

try:  # Lightweight fallback if WeasyPrint is unavailable
    from reportlab.lib.pagesizes import A4  # type: ignore
    from reportlab.pdfgen import canvas  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    A4 = None  # type: ignore
    canvas = None  # type: ignore

if TYPE_CHECKING:  # pragma: no cover - hints only
    from ..models import Note, Patient


_TEMPLATE_ROOT = Path(__file__).resolve().parent.parent / 'templates' / 'pdf'
_ENV = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_ROOT)),
    autoescape=select_autoescape(['html', 'xml'])
)

_MISSING = '??'


def _as_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    to_dict = getattr(value, 'to_dict', None)
    if callable(to_dict):
        return to_dict()
    return {}


def _normalize_vitals(raw: Dict[str, Any]) -> Dict[str, Any]:
    defaults = {
        'temp': _MISSING,
        'hr': _MISSING,
        'rr': _MISSING,
        'bp_sys': _MISSING,
        'bp_dia': _MISSING,
        'spo2': _MISSING,
    }
    for key in defaults:
        value = raw.get(key)
        defaults[key] = value if value not in (None, '') else _MISSING
    return defaults


def _normalize_medications(items: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    meds: List[Dict[str, Any]] = []
    if not items:
        return meds
    for item in items:
        meds.append({
            'name': item.get('name') or _MISSING,
            'dose': item.get('dose') or _MISSING,
            'route': item.get('route') or _MISSING,
            'time': item.get('time') or _MISSING,
        })
    return meds


def _fallback(value: Any) -> Any:
    return value if value not in (None, '') else _MISSING


def _render_with_reportlab(context: Dict[str, Any]) -> bytes:
    if canvas is None or A4 is None:
        raise RuntimeError('pdf_renderer_unavailable')

    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 40

    def line(text: str = '', step: int = 16) -> None:
        nonlocal y
        pdf.drawString(40, y, text)
        y -= step
        if y < 60:
            pdf.showPage()
            y = height - 40

    note = context['note']
    patient = context['patient']

    line(f"CareNotes - Note #{_fallback(note.get('id'))}", step=20)
    line(f"Generated: {context['generated_at']}")
    line(f"Patient: {patient.get('name', _MISSING)} (ID {patient.get('id', _MISSING)})")
    line(f"Ward/Bed: {patient.get('ward', _MISSING)} / {patient.get('bed', _MISSING)}")
    line(f"MRN: {patient.get('mrn', _MISSING)}  Gender: {patient.get('gender', _MISSING)}  DOB: {patient.get('dob', _MISSING)}")
    line('-' * 90, step=18)

    vitals = context['vitals']
    line('Vitals:', step=18)
    line(f"  Temp: {vitals['temp']}  HR: {vitals['hr']}  RR: {vitals['rr']}")
    line(f"  BP: {vitals['bp_sys']}/{vitals['bp_dia']}  SpO2: {vitals['spo2']}")
    line(f"Pain: {context['pain']}    Intake: {context['intake']} ml    Output: {context['output']} ml", step=18)

    line('SOAP:', step=18)
    line(f"  S: {context['subjective']}")
    line(f"  O: {context['objective']}")
    line(f"  A: {context['assessment']}")
    line(f"  P: {context['plan']}")
    line()

    line('Medications:', step=18)
    meds = context['medications'] or [{
        'name': _MISSING,
        'dose': _MISSING,
        'route': _MISSING,
        'time': _MISSING,
    }]
    for med in meds:
        line(f"  - {med['name']} | {med['dose']} | {med['route']} | {med['time']}")
    line()

    alerts = context['alerts'] or []
    line('Alerts:', step=18)
    if alerts:
        for alert in alerts:
            line(f"  - {alert}")
    else:
        line('  (none)')

    pdf.showPage()
    pdf.save()
    return buf.getvalue()


def generate_note_pdf(note: 'Note | Dict[str, Any]', *, patient: 'Patient | Dict[str, Any] | None' = None) -> bytes:
    """Render the care note PDF using the bundled HTML template."""
    note_dict = _as_dict(note)
    patient_dict = _as_dict(patient)

    vitals = _normalize_vitals(note_dict.get('vitals') or {})
    medications = _normalize_medications(note_dict.get('med_given'))
    alerts = note_dict.get('alerts') or []

    context = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'patient': patient_dict,
        'note': note_dict,
        'vitals': vitals,
        'intake': _fallback(note_dict.get('intake_ml')),
        'output': _fallback(note_dict.get('output_ml')),
        'pain': _fallback(note_dict.get('pain_score')),
        'subjective': _fallback(note_dict.get('subjective')),
        'objective': _fallback(note_dict.get('objective')),
        'assessment': _fallback(note_dict.get('assessment')),
        'plan': _fallback(note_dict.get('plan')),
        'medications': medications,
        'alerts': alerts,
    }

    if HTML is not None:
        template = _ENV.get_template('note.html')
        html = template.render(**context)
        return HTML(string=html, base_url=str(_TEMPLATE_ROOT)).write_pdf()

    return _render_with_reportlab(context)


__all__ = ['generate_note_pdf']
