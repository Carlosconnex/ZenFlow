from . import db  # This refers to the db initialized in your __init__.py


class ProjectBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    archived = db.Column(db.Boolean, default=False, nullable=False)
    tasks = db.relationship(
        'Task',
        backref='board',
        lazy=True,
        cascade='all, delete-orphan'
    )


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    status = db.Column(db.String(20), default='todo')  # todo, doing, done
    energy_level = db.Column(db.Integer, default=1)    # 1=Easy, 2=Medium, 3=Deep Work
    board_id = db.Column(db.Integer, db.ForeignKey('project_board.id'), nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     status = db.Column(db.String(20), default='todo') # todo, doing, done
#     energy_level = db.Column(db.Integer, default=1) # 1=Easy, 2=Medium, 3=Deep Work
