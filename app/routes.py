from flask import Blueprint, render_template, request, redirect, url_for
from .models import Board, List, Card
from . import db, APP_NAME, VERSION

main = Blueprint('main', __name__)

@main.route("/")
def home():
    # The home page now shows all available boards
    boards = Board.query.all()
    return render_template("index.html", boards=boards, name=APP_NAME, ver=VERSION)

@main.route("/board/<int:board_id>")
def view_board(board_id):
    # View a specific Kanban board
    board = db.get_or_404(Board, board_id)
    return render_template("board.html", board=board, name=APP_NAME, ver=VERSION)

@main.route("/add_board", methods=['POST'])
def add_board():
    title = request.form.get('title')
    if title:
        new_board = Board(title=title)
        db.session.add(new_board)
        db.session.commit()
    return redirect(url_for('main.home'))

@main.route("/add_list/<int:board_id>", methods=['POST'])
def add_list(board_id):
    title = request.form.get('title')
    if title:
        new_list = List(title=title, board_id=board_id)
        db.session.add(new_list)
        db.session.commit()
    return redirect(url_for('main.view_board', board_id=board_id))

@main.route("/add_card/<int:list_id>", methods=['POST'])
def add_card(list_id):
    content = request.form.get('content')
    energy = request.form.get('energy_level', 1)
    # We fetch the list to find the board_id for the redirect
    parent_list = db.get_or_404(List, list_id)
    if content:
        new_card = Card(content=content, energy_level=int(energy), list_id=list_id)
        db.session.add(new_card)
        db.session.commit()
    return redirect(url_for('main.view_board', board_id=parent_list.board_id))

@main.route("/move_card/<int:card_id>/<int:new_list_id>")
def move_card(card_id, new_list_id):
    # 1. Find the card
    card = db.get_or_404(Card, card_id)
    
    # 2. Update its list_id to the new destination
    card.list_id = new_list_id
    db.session.commit()
    
    # 3. Find which board this list belongs to so we can redirect back to it
    return redirect(url_for('main.view_board', board_id=card.list.board_id))