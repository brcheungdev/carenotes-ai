from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ''}:  # allow running via `python backend/app.py`
    project_root = Path(__file__).resolve().parent.parent
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    __package__ = 'backend'

from flask import Flask, jsonify
from flask_cors import CORS

from .config import settings
from .db import db
from .routes import register_error_handlers
from .routes.auth import auth_bp
from .routes.patients import patients_bp
from .routes.notes import notes_bp
from .routes.export import export_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.MYSQL_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)
    register_error_handlers(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patients_bp, url_prefix='/api/patients')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')
    app.register_blueprint(export_bp, url_prefix='/api/export')

    @app.route('/')
    def root():
        return jsonify({'ok': True, 'version': 'mvp'})

    return app


app = create_app()


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
