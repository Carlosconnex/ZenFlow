from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import Task, ProjectBoard
from . import db, APP_NAME, VERSION, DESCRIPTION

main = Blueprint('main', __name__)

# --- TEAM CONSTANTS & UTILITIES ---
_STATUS_ALIASES = {
    'start': 'doing',
    'doing': 'doing',
    'todo': 'todo',
    'done': 'done',
}

def _normalize_status(value):
    return _STATUS_ALIASES.get(value)


def _normalize_complexity(raw_value):
    if raw_value is None:
        return 2

    value = str(raw_value).strip().lower()
    complexity_map = {
        '1': 1,
        '2': 2,
        '3': 3,
        'low': 1,
        'medium': 2,
        'high': 3,
        'easy': 1,
        'deep work': 3,
    }
    return complexity_map.get(value, 2)

# --- DASHBOARD & BOARD LISTING ---
@main.route('/')
def landing():
    # Only non-archived boards on dashboard
    boards = ProjectBoard.query.filter_by(archived=False).order_by(ProjectBoard.id.asc()).all()
    first_board_id = boards[0].id if boards else None

    # Team logic: Backfill tasks without a board_id to the first board
    if first_board_id is not None and Task.query.filter(Task.board_id.is_(None)).first() is not None:
        Task.query.filter(Task.board_id.is_(None)).update({'board_id': first_board_id})
        db.session.commit()

    # Calculate stats for the dashboard cards (only non-archived tasks)
    board_cards = []
    for board in boards:
        tasks = Task.query.filter_by(board_id=board.id, archived=False).all()
        board_cards.append({
            'id': board.id,
            'name': board.name,
            'total': len(tasks),
            'todo': sum(1 for task in tasks if task.status == 'todo'),
            'doing': sum(1 for task in tasks if task.status == 'doing'),
            'done': sum(1 for task in tasks if task.status == 'done'),
        })

    return render_template(
        'landing.html',
        name=APP_NAME,
        desc=DESCRIPTION,
        ver=VERSION,
        boards=board_cards,
        first_board_id=first_board_id,
    )

@main.route('/boards', methods=['POST'])
def create_board():
    """Team's primary route for creating new boards."""
    board_name = (request.form.get('board_name') or '').strip()
    if not board_name:
        return redirect(url_for('main.landing'))

    existing = ProjectBoard.query.filter_by(name=board_name).first()
    if existing:
        return redirect(url_for('main.board_view', board_id=existing.id))

    board = ProjectBoard(name=board_name)
    db.session.add(board)
    db.session.commit()

    # Backfill logic for newly created boards if it's the only one
    if ProjectBoard.query.count() == 1 and Task.query.filter(Task.board_id.is_(None)).first() is not None:
        Task.query.filter(Task.board_id.is_(None)).update({'board_id': board.id})
        db.session.commit()

    return redirect(url_for('main.board_view', board_id=board.id))

# --- KANBAN VIEW & TASK ACTIONS ---
@main.route('/boards/<int:board_id>')
def board_view(board_id):
    """Renders the team's Kanban board (index.html)."""
    board = db.get_or_404(ProjectBoard, board_id)
    if board.archived:
        return redirect(url_for('main.meadow'))
    tasks = Task.query.filter_by(board_id=board.id, archived=False).all()

    return render_template(
        'index.html',
        name=APP_NAME,
        desc=DESCRIPTION,
        ver=VERSION,
        board=board,
        tasks=tasks,
    )

@main.route('/boards/<int:board_id>/add', methods=['POST'])
def add_task(board_id):
    board = db.get_or_404(ProjectBoard, board_id)
    title = (request.form.get('title') or request.form.get('content') or '').strip()
    description = (request.form.get('description') or '').strip()
    complexity = request.form.get('complexity', request.form.get('energy_level', 2))

    if title:
        new_task = Task(
            content=title,
            description=description,
            status='todo',
            energy_level=_normalize_complexity(complexity),
            board_id=board.id,
        )
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('main.board_view', board_id=board.id))


@main.route('/boards/<int:board_id>/tasks/<int:task_id>/edit', methods=['POST'])
def edit_task(board_id, task_id):
    board = db.get_or_404(ProjectBoard, board_id)
    task = Task.query.filter_by(id=task_id, board_id=board.id).first_or_404()

    title = (request.form.get('title') or '').strip()
    if title:
        task.content = title

    task.description = (request.form.get('description') or '').strip()
    complexity = request.form.get('complexity', request.form.get('energy_level', task.energy_level))
    task.energy_level = _normalize_complexity(complexity)

    db.session.commit()
    return redirect(url_for('main.board_view', board_id=board.id))

@main.route('/boards/<int:board_id>/move/<int:id>/<string:new_status>')
def move_task(board_id, id, new_status):
    board = db.get_or_404(ProjectBoard, board_id)
    task = Task.query.filter_by(id=id, board_id=board.id).first_or_404()
    normalized_status = _normalize_status(new_status)

    if normalized_status is None:
        return redirect(url_for('main.board_view', board_id=board.id))

    task.status = normalized_status
    db.session.commit()
    return redirect(url_for('main.board_view', board_id=board.id))

@main.route('/api/boards/<int:board_id>/tasks/<int:id>/move', methods=['POST'])
def move_task_api(board_id, id):
    """API for drag-and-drop support."""
    board = db.get_or_404(ProjectBoard, board_id)
    task = Task.query.filter_by(id=id, board_id=board.id).first_or_404()
    payload = request.get_json(silent=True) or {}
    normalized_status = _normalize_status(payload.get('new_status'))

    if normalized_status is None:
        return jsonify({'ok': False, 'error': 'Invalid status'}), 400

    task.status = normalized_status
    db.session.commit()
    return jsonify({
        'ok': True,
        'task_id': task.id,
        'board_id': board.id,
        'new_status': task.status,
    })

@main.route('/boards/<int:board_id>/delete/<int:id>')
def delete_task(board_id, id):
    board = db.get_or_404(ProjectBoard, board_id)
    task = Task.query.filter_by(id=id, board_id=board.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.board_view', board_id=board.id))

# --- THE MEADOW (Archive) ---
@main.route('/meadow')
def meadow():
    """The Meadow: archive view for old cards and boards."""
    archived_tasks = (
        Task.query.filter_by(archived=True)
        .order_by(Task.id.desc())
        .all()
    )
    archived_boards = (
        ProjectBoard.query.filter_by(archived=True)
        .order_by(ProjectBoard.id.desc())
        .all()
    )
    return render_template(
        'meadow.html',
        name=APP_NAME,
        desc=DESCRIPTION,
        ver=VERSION,
        archived_tasks=archived_tasks,
        archived_boards=archived_boards,
    )


@main.route('/api/tasks/<int:task_id>/archive', methods=['POST'])
def archive_task_api(task_id):
    task = Task.query.filter_by(id=task_id).first_or_404()
    task.archived = True
    db.session.commit()
    return jsonify({'ok': True, 'task_id': task.id})


@main.route('/api/tasks/<int:task_id>/unarchive', methods=['POST'])
def unarchive_task_api(task_id):
    task = Task.query.filter_by(id=task_id).first_or_404()
    task.archived = False
    db.session.commit()
    return jsonify({'ok': True, 'task_id': task.id, 'board_id': task.board_id})


@main.route('/api/boards/<int:board_id>/archive', methods=['POST'])
def archive_board_api(board_id):
    board = db.get_or_404(ProjectBoard, board_id)
    board.archived = True
    db.session.commit()
    return jsonify({'ok': True, 'board_id': board.id})


@main.route('/api/boards/<int:board_id>/unarchive', methods=['POST'])
def unarchive_board_api(board_id):
    board = db.get_or_404(ProjectBoard, board_id)
    board.archived = False
    db.session.commit()
    return jsonify({'ok': True, 'board_id': board.id})


# --- LEGACY & EXTRA ROUTES ---
@main.route('/board')
def board_legacy_redirect():
    first_board = ProjectBoard.query.filter_by(archived=False).order_by(ProjectBoard.id.asc()).first()
    if first_board is None:
        return redirect(url_for('main.landing'))
    return redirect(url_for('main.board_view', board_id=first_board.id))

@main.route('/second')
def second():
    return '<h1><a href="/">Go back home</a></h1>'

@main.route('/third')
def third():
    return '<h1><a href="/">Go back home</a></h1>'

@main.route('/api/boards/<int:board_id>/update', methods=['POST'])
def update_board_api(board_id):
    """API for updating board name."""
    board = db.get_or_404(ProjectBoard, board_id)
    payload = request.get_json(silent=True) or {}
    new_name = (payload.get('name') or '').strip()

    if not new_name:
        return jsonify({'ok': False, 'error': 'Board name cannot be empty'}), 400

    existing = ProjectBoard.query.filter(
        ProjectBoard.name == new_name,
        ProjectBoard.id != board.id,
    ).first()
    if existing:
        return jsonify({'ok': False, 'error': 'A board with this name already exists'}), 400

    board.name = new_name
    db.session.commit()
    return jsonify({'ok': True, 'name': board.name})


@main.route('/boards/<int:board_id>/delete', methods=['POST'])
def delete_board(board_id):
    board = db.get_or_404(ProjectBoard, board_id)
    
    # Delete all tasks associated with this board first
    Task.query.filter_by(board_id=board.id).delete()
    
    # Delete the board itself
    db.session.delete(board)
    db.session.commit()
    
    return redirect(url_for('main.landing'))
