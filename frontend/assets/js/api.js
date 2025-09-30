import { getToken } from './auth.js';

let API_BASE = localStorage.getItem('API_BASE') || 'http://127.0.0.1:5000/api';

export function setApiBase(url) {
    API_BASE = url;
    if (url) {
        localStorage.setItem('API_BASE', url);
    } else {
        localStorage.removeItem('API_BASE');
    }
}

async function request(path, { method = 'GET', body, headers = {}, multipart = false } = {}) {
    const token = getToken();
    const finalHeaders = new Headers(headers);
    if (!multipart) {
        finalHeaders.set('Content-Type', 'application/json');
    }
    if (token) {
        finalHeaders.set('Authorization', `Bearer ${token}`);
    }

    const url = `${API_BASE}${path}`;
    const options = { method, headers: finalHeaders }; 
    if (body !== undefined) {
        options.body = multipart ? body : JSON.stringify(body);
    }

    const response = await fetch(url, options);
    if (!response.ok) {
        let errorPayload;
        try {
            errorPayload = await response.json();
        } catch (_) {
            throw new Error(`HTTP ${response.status}`);
        }
        const message = errorPayload?.error?.message || `HTTP ${response.status}`;
        const code = errorPayload?.error?.code || 'error';
        const err = new Error(message);
        err.code = code;
        err.status = response.status;
        throw err;
    }

    if (response.status === 204) {
        return null;
    }

    const contentType = response.headers.get('Content-Type') || '';
    if (contentType.includes('application/json')) {
        return response.json();
    }
    return response;
}

export function get(path) {
    return request(path, { method: 'GET' });
}

export function post(path, body, opts = {}) {
    const { multipart = false } = opts;
    return request(path, { method: 'POST', body, multipart });
}

export async function download(path) {
    const token = getToken();
    const url = `${API_BASE}${path}`;
    const headers = new Headers();
    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }
    const response = await fetch(url, { headers });
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    return response.blob();
}

export { API_BASE };

