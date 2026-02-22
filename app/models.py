from . import db
from datetime import datetime

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # Relationship: One Board -> Many Lists
    lists = db.relationship('List', backref='board', lazy=True, cascade="all, delete-orphan")

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    # Relationship: One List -> Many Cards
    cards = db.relationship('Card', backref='list', lazy=True, cascade="all, delete-orphan")

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    energy_level = db.Column(db.Integer, default=1)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)