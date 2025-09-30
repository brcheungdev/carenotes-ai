import { post } from './api.js';

const TOKEN_KEY = 'carenotes_token';
const PAYLOAD_KEY = 'carenotes_payload';

export async function login(username, password) {
    const result = await post('/auth/login', { username, password });
    const { data } = result || {};
    if (!data?.token) {
        throw new Error('login_failed');
    }
    localStorage.setItem(TOKEN_KEY, data.token);
    localStorage.setItem(PAYLOAD_KEY, JSON.stringify(data.payload));
}

export function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(PAYLOAD_KEY);
}

export function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

export function getUser() {
    const payload = localStorage.getItem(PAYLOAD_KEY);
    if (!payload) return null;
    try {
        return JSON.parse(payload);
    } catch (_) {
        return null;
    }
}

export function isAuthed() {
    return Boolean(getToken());
}
