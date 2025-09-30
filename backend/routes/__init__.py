from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple

import jwt
from flask import Flask, Response, current_app, g, jsonify, request

from ..config import settings


class APIError(Exception):
    status_code = 400
    code = 'bad_request'
    message = 'bad_request'

    def __init__(self, message: Optional[str] = None, *, code: Optional[str] = None, status_code: Optional[int] = None):
        super().__init__(message or self.message)
        if message:
            self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code

    def to_response(self) -> Tuple[Response, int]:
        payload = {
            'ok': False,
            'error': {
                'code': self.code,
                'message': self.message,
            },
        }
        return jsonify(payload), self.status_code


class UnauthorizedError(APIError):
    status_code = 401
    code = 'unauthorized'
    message = 'invalid_token'


class ForbiddenError(APIError):
    status_code = 403
    code = 'forbidden'
    message = 'insufficient_role'


class NotFoundError(APIError):
    status_code = 404
    code = 'not_found'
    message = 'not_found'


class ConflictError(APIError):
    status_code = 409
    code = 'conflict'
    message = 'conflict'


class UnprocessableError(APIError):
    status_code = 422
    code = 'unprocessable'
    message = 'unprocessable'


class ServerError(APIError):
    status_code = 500
    code = 'server_error'
    message = 'server_error'


def success_response(data: Any = None, *, meta: Optional[Dict[str, Any]] = None, status_code: int = 200):
    payload: Dict[str, Any] = {'ok': True}
    if data is not None:
        payload['data'] = data
    if meta is not None:
        payload['meta'] = meta
    return jsonify(payload), status_code


@dataclass(slots=True)
class AuthContext:
    username: str
    role: str
    payload: Dict[str, Any]


def issue_token(username: str, role: str) -> Dict[str, Any]:
    now = int(time.time())
    payload = {
        'sub': username,
        'role': role,
        'iat': now,
        'exp': now + 3600,
        'jti': str(uuid.uuid4()),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return {'token': token, 'payload': payload}


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedError('token_expired') from exc
    except jwt.PyJWTError as exc:
        raise UnauthorizedError('invalid_token') from exc
    return payload


def token_required(role: Optional[str] = None):
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                raise UnauthorizedError('invalid_token')
            token = auth_header.split(' ', 1)[1].strip()
            payload = decode_token(token)
            username = payload.get('sub')
            role_value = payload.get('role', '')
            if role and role_value != role:
                raise ForbiddenError()
            g.current_user = AuthContext(username=username, role=role_value, payload=payload)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def register_error_handlers(app: "Flask"):
    @app.errorhandler(APIError)
    def _handle_api_error(err: APIError):
        return err.to_response()

    @app.errorhandler(Exception)
    def _handle_generic_error(err: Exception):  # pragma: no cover - defensive
        current_app.logger.exception('Unhandled exception: %s', err)
        api_err = ServerError(str(err))
        return api_err.to_response()


__all__ = [
    'APIError',
    'UnauthorizedError',
    'ForbiddenError',
    'NotFoundError',
    'ConflictError',
    'UnprocessableError',
    'ServerError',
    'success_response',
    'token_required',
    'register_error_handlers',
    'issue_token',
]
