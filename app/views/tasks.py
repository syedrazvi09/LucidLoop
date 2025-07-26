from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models import db, Task, User
from datetime import datetime, timezone

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


# Helper: Redirect if not logged in
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


@tasks_bp.route('/')
def all_tasks():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login_page'))
    
    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.due_date).all()
    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/add', methods=['POST'])
def add_task():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    data = request.form
    new_task = Task(
        title=data.get('title'),
        category=data.get('category'),
        due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%dT%H:%M') if data.get('due_date') else None,
        priority=data.get('priority'),
        notes=data.get('notes'),
        user_id=user.id,
        predicted_best_time=data.get('predicted_best_time') or "N/A"
    )

    db.session.add(new_task)
    db.session.commit()
    flash("Task added successfully!")
    return redirect(url_for('tasks.all_tasks'))


@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        flash("Unauthorized!")
        return redirect(url_for('tasks.all_tasks'))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.")
    return redirect(url_for('tasks.all_tasks'))


@tasks_bp.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        flash("Unauthorized!")
        return redirect(url_for('tasks.all_tasks'))

    task.is_done = True
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    flash("Task marked as complete.")
    return redirect(url_for('tasks.all_tasks'))


@tasks_bp.route('/backlog')
def backlog_tasks():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    tasks = Task.query.filter_by(user_id=user.id, is_done=False).order_by(Task.due_date).all()
    return render_template('backlog.html', tasks=tasks)


@tasks_bp.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        flash("Unauthorized!")
        return redirect(url_for('tasks.all_tasks'))

    if request.method == 'POST':
        data = request.form
        task.title = data.get('title')
        task.category = data.get('category')
        task.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%dT%H:%M') if data.get('due_date') else None
        task.priority = data.get('priority')
        task.notes = data.get('notes')
        task.predicted_best_time = data.get('predicted_best_time') or task.predicted_best_time
        db.session.commit()
        flash("Task updated.")
        return redirect(url_for('tasks.all_tasks'))

    return render_template('update_task.html', task=task)
