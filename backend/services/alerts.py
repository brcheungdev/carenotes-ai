from __future__ import annotations

from typing import Dict, List, Optional


_ALERT_MESSAGES = {
    'temp_high': '体温异常 ≥38°C',
    'temp_low': '体温异常 ≤35°C',
    'hr_high': '心率异常 ≥120bpm',
    'hr_low': '心率异常 ≤50bpm',
    'bp_sys_high': '收缩压异常 ≥180mmHg',
    'bp_sys_low': '收缩压异常 ≤90mmHg',
    'bp_dia_high': '舒张压异常 ≥110mmHg',
    'spo2_low': '血氧饱和度 ≤92%',
}


def _ensure_float(value: Optional[float | int]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def detect_alerts(vitals: Optional[Dict[str, Optional[float | int]]]) -> List[str]:
    if not vitals:
        return []

    alerts: List[str] = []

    temp = _ensure_float(vitals.get('temp'))
    if temp is not None:
        if temp >= 38.0:
            alerts.append(_ALERT_MESSAGES['temp_high'])
        if temp <= 35.0:
            alerts.append(_ALERT_MESSAGES['temp_low'])

    hr = _ensure_float(vitals.get('hr'))
    if hr is not None:
        if hr >= 120:
            alerts.append(_ALERT_MESSAGES['hr_high'])
        if hr <= 50:
            alerts.append(_ALERT_MESSAGES['hr_low'])

    bp_sys = _ensure_float(vitals.get('bp_sys'))
    if bp_sys is not None:
        if bp_sys >= 180:
            alerts.append(_ALERT_MESSAGES['bp_sys_high'])
        if bp_sys <= 90:
            alerts.append(_ALERT_MESSAGES['bp_sys_low'])

    bp_dia = _ensure_float(vitals.get('bp_dia'))
    if bp_dia is not None and bp_dia >= 110:
        alerts.append(_ALERT_MESSAGES['bp_dia_high'])

    spo2 = _ensure_float(vitals.get('spo2'))
    if spo2 is not None and spo2 <= 92:
        alerts.append(_ALERT_MESSAGES['spo2_low'])

    seen = set()
    deduped = []
    for item in alerts:
        if item not in seen:
            deduped.append(item)
            seen.add(item)
    return deduped


__all__ = ['detect_alerts']
