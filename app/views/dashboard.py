from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from models import db, Task, SubTask, User

bp = Blueprint('dashboard', __name__)

# Temporary user session simulation
def get_current_user_id():
    return session.get('user_id', 1)  # Default to user ID 1 for now

@bp.route('/')
def home():
    user_id = get_current_user_id()
    today = datetime.today().date()

    tasks_today = Task.query.filter_by(user_id=user_id).filter(Task.due_date == today).all()
    backlog_tasks = Task.query.filter_by(user_id=user_id).filter(Task.due_date < today, Task.is_done == False).all()
    all_tasks = Task.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html',
                           tasks_today=tasks_today,
                           backlog_tasks=backlog_tasks,
                           all_tasks=all_tasks)


@bp.route('/add-task', methods=['POST'])
def add_task():
    try:
        title = request.form.get('title', '').strip()
        due_date_str = request.form.get('due_date', '')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        priority = request.form.get('priority', 'Medium')
        category = request.form.get('category', '').strip()
        notes = request.form.get('notes', '').strip()

        reminder_time_str = request.form.get('reminder_time', '')
        reminder_time = None
        if reminder_time_str:
            try:
                # Parse full datetime-local input and extract only the time part
                reminder_time = datetime.strptime(reminder_time_str, "%Y-%m-%dT%H:%M").time()
            except ValueError as ve:
                print(f"Reminder time format error: {ve}")
                flash("Invalid reminder time format", "danger")

        is_recurring = request.form.get('is_recurring') == 'on'
        recurrence_pattern = request.form.get('recurrence_pattern', '').strip()

        task = Task(
            title=title,
            due_date=due_date,
            priority=priority,
            category=category,
            notes=notes,
            reminder_time=reminder_time,
            is_recurring=is_recurring,
            recurrence_pattern=recurrence_pattern,
            user_id=get_current_user_id()
        )
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully!", "success")

    except Exception as e:
        print("Add task error:", e)
        flash(f"Error adding task: {str(e)}", "danger")

    return redirect(url_for('dashboard.home'))


@bp.route('/complete-task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = True
    task.completed_at = datetime.now()
    db.session.commit()
    flash("Task marked as completed!", "info")
    return redirect(url_for('dashboard.home'))

@bp.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "warning")
    return redirect(url_for('dashboard.home'))

@bp.route('/add-subtask/<int:task_id>', methods=['POST'])
def add_subtask(task_id):
    title = request.form.get('subtask_title', '').strip()
    if not title:
        flash("Subtask title is required.", "danger")
        return redirect(url_for('dashboard.home'))

    subtask = SubTask(title=title, task_id=task_id)
    db.session.add(subtask)
    db.session.commit()
    flash("Subtask added!", "success")
    return redirect(url_for('dashboard.home'))

@bp.route('/complete-subtask/<int:subtask_id>', methods=['POST'])
def complete_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    subtask.is_done = True
    db.session.commit()
    flash("Subtask completed!", "info")
    return redirect(url_for('dashboard.home'))

@bp.route('/delete-subtask/<int:subtask_id>', methods=['POST'])
def delete_subtask(subtask_id):
    subtask = SubTask.query.get_or_404(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    flash("Subtask deleted!", "warning")
    return redirect(url_for('dashboard.home'))
