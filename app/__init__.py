from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

# Constants
APP_NAME = "ZenFlow"
VERSION = "1.1"
DESCRIPTION = "Consolidated Task Manager"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zenflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        _ensure_task_board_column()
        _ensure_archived_columns()
        _ensure_task_description_column()

    return app


def _ensure_task_board_column():
    # Lightweight schema backfill for existing SQLite DBs without Alembic.
    inspector = db.session.execute(text("PRAGMA table_info(task)")).fetchall()
    if not inspector:
        return

    column_names = {row[1] for row in inspector}
    if 'board_id' not in column_names:
        db.session.execute(text("ALTER TABLE task ADD COLUMN board_id INTEGER"))
        db.session.commit()


def _ensure_archived_columns():
    """Add archived column to task and project_board if missing (The Meadow)."""
    try:
        task_info = db.session.execute(text("PRAGMA table_info(task)")).fetchall()
        task_cols = {row[1] for row in task_info}
        if task_info and 'archived' not in task_cols:
            db.session.execute(text("ALTER TABLE task ADD COLUMN archived INTEGER DEFAULT 0"))
        board_info = db.session.execute(text("PRAGMA table_info(project_board)")).fetchall()
        board_cols = {row[1] for row in board_info}
        if board_info and 'archived' not in board_cols:
            db.session.execute(text("ALTER TABLE project_board ADD COLUMN archived INTEGER DEFAULT 0"))
        db.session.commit()
    except Exception:
        db.session.rollback()


def _ensure_task_description_column():
    inspector = db.session.execute(text("PRAGMA table_info(task)")).fetchall()
    if not inspector:
        return

    column_names = {row[1] for row in inspector}
    if 'description' not in column_names:
        db.session.execute(text("ALTER TABLE task ADD COLUMN description TEXT DEFAULT ''"))
        db.session.commit()
