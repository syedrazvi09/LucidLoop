from flask import Blueprint, render_template, session, redirect, url_for
from app.models import User

pomodoro_bp = Blueprint(
    'pomodoro',
    __name__,
    url_prefix='/pomodoro',
    template_folder='../../templates'
)

def get_current_user():
    user_id = session.get('user_id')
    return User.query.get(user_id) if user_id else None

@pomodoro_bp.route('/timer')
def timer():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login_page'))
    return render_template('timer.html', username=user.username)
