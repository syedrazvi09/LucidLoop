from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from app import db
from app.models import Reminder, User

reminders_bp = Blueprint('reminders', __name__, url_prefix='/reminders')

# View all reminders
@reminders_bp.route('/', methods=['GET'])
def reminders():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    reminders = Reminder.query.filter_by(user_id=user_id).order_by(Reminder.remind_at).all()
    return render_template('reminders.html', reminders=reminders)


# Add a new reminder
@reminders_bp.route('/add', methods=['POST'])
def add_reminder():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    message = request.form.get('message')
    remind_at_str = request.form.get('remind_at')

    try:
        remind_at = datetime.strptime(remind_at_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        return "Invalid datetime format", 400

    reminder = Reminder(user_id=user_id, message=message, remind_at=remind_at)
    db.session.add(reminder)
    db.session.commit()

    return redirect(url_for('reminders.reminders'))


# Delete a reminder
@reminders_bp.route('/delete/<int:reminder_id>', methods=['POST'])
def delete_reminder(reminder_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    reminder = Reminder.query.get_or_404(reminder_id)

    if reminder.user_id != session['user_id']:
        return "Unauthorized", 403

    db.session.delete(reminder)
    db.session.commit()
    return redirect(url_for('reminders.reminders'))
