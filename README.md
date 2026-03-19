# IT-111 Course Project using Flask

- **Version:** 0.1.0

## Project Overview
### ZenFlow: ADHD-Friendly Task Tracker
The ZenFlow project is a Flask-based web app designed to provide visual, low-stress environment for managing tasks. By utilizing a 'Kanban' style interface, it allows users to break down overwhelming tasks into manageable stages.

## MVP (Minimum Viable Product)
Our application, "ZenFlow" is a visual task management tool designed to help users with ADHD, or folks who need a little encouragement, organize their daily and weekly responsibilities without the clutter of traditional planners. The app solves the problem of "out of sight - out of mind" by providing a visual ‘Kanban’ board interface. The intended user is anyone who struggles with keeping track or simply prefers visual progress tracking. The primary action a user can take is creating task "cards" and moving it between "To-Do," "In Progress," and "Complete" columns; these are fully customizable based on the user's preference. 

### MVP Deliverables
The ZenFlow app will focus on local session-based task management, allowing users to see their progress in real time within a single “Flow” dashboard. We will focus on the core visual experience of task tracking. Users will be able to create task-cards with descriptions, and be able to move them across three primary columns; "To-Do", "In Progress", "Completed". This version prioritizes simplicity and immediate visual feedback to assist users with executive function challenges.

### Planned Features
- Visual Kanban Board
- Task Creation/Deletion
- Achievement/Reward System for completed tasks
- Reminder Notifications

## Functional Requirements
- Create “Cards”: The user must be able to create a “card”
- Create Tasks: The user must be able to input a task title and description.
- Categorize: The application must sort tasks into various custom columns: To-Do, In Progress, Review, Completed, etc.
- Visual Layout: The app must display these tasks side-by-side in a Kanban format.
- Update Status: The user must be able to change the status of a task (moving it to another column).

## Non-functional Requirements
- Usability: The interface should be clean and minimize distractions (ADHD-friendly).
- Performance: The board should update instantly when a task is added/completed.
- Environment: The app must run on Flask 3 and Python 3.10+ .


## How to run the app

1. Clone the repo

```bash
git clone <repository-url>
cd <repository-folder>
```

2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install Flask
```

4. Run the app

```bash
python{version_number} app.py
```

5. Open the browser and visit: http://127.0.0.1:5000

## Technology Used

- Python 3
- Flask
