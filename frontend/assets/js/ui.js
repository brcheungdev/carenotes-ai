export function renderAlertsBadges(alerts = []) {
    const wrapper = document.createElement('div');
    wrapper.className = 'flex-row';
    if (!alerts.length) {
        const badge = document.createElement('span');
        badge.className = 'badge';
        badge.textContent = '无警报';
        wrapper.appendChild(badge);
        return wrapper;
    }
    alerts.forEach((alert) => {
        const badge = document.createElement('span');
        badge.className = 'badge alert';
        badge.textContent = alert;
        wrapper.appendChild(badge);
    });
    return wrapper;
}

export function renderVitalsSummary(vitals = {}, pain = null, io = {}) {
    const fields = [
        { label: 'Temp (°C)', value: safe(vitals.temp) },
        { label: 'HR (bpm)', value: safe(vitals.hr) },
        { label: 'RR (bpm)', value: safe(vitals.rr) },
        { label: 'BP (S/D)', value: vitals.bp_sys && vitals.bp_dia ? `${vitals.bp_sys}/${vitals.bp_dia}` : '—' },
        { label: 'SpO₂ (%)', value: safe(vitals.spo2) },
        { label: 'Pain', value: safe(pain) },
        { label: 'I/O (ml)', value: `${safe(io.intake_ml)}/${safe(io.output_ml)}` },
    ];
    return fields
        .map((field) => `<span><strong>${field.label}</strong><br>${field.value}</span>`)
        .join('');
}

function safe(value) {
    if (value === null || value === undefined || value === '') {
        return '—';
    }
    return value;
}

const toastContainerId = 'toast-container';

function ensureToastContainer() {
    let container = document.getElementById(toastContainerId);
    if (!container) {
        container = document.createElement('div');
        container.id = toastContainerId;
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    return container;
}

export function toast(message, type = 'info', duration = 3000) {
    const container = ensureToastContainer();
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.textContent = message;
    container.appendChild(el);
    setTimeout(() => {
        el.remove();
        if (!container.children.length) {
            container.remove();
        }
    }, duration);
}

export function confirm(message) {
    return Promise.resolve(window.confirm(message));
}
