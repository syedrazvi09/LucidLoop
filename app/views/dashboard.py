from flask import Blueprint, render_template, session, redirect, url_for
from app.models import User

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def dashboard_home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    
    user = User.query.get(session['user_id'])
    
    return render_template('dashboard.html', username=user.username)


@dashboard_bp.route('/view')
def tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    
    # Tasks from DB
    tasks = ['Train CNN on dataset', 'Optimize hyperparameters', 'Analyze model logs']
    return render_template('tasks.html', tasks=tasks)

