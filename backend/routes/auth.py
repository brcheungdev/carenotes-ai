from __future__ import annotations

from flask import Blueprint, request

from . import APIError, UnauthorizedError, issue_token, success_response


auth_bp = Blueprint('auth', __name__)


_DEMO_USERS = {
    'nurse': {'password': 'Passw0rd!', 'role': 'nurse'},
    'admin': {'password': 'Passw0rd!', 'role': 'admin'},
}


@auth_bp.post('/login')
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''
    if not username or not password:
        raise APIError('missing_credentials', code='bad_request', status_code=400)

    account = _DEMO_USERS.get(username)
    if not account or account['password'] != password:
        raise UnauthorizedError('invalid_credentials')

    issued = issue_token(username, account['role'])
    data = {'token': issued['token'], 'payload': issued['payload']}
    return success_response(data)
