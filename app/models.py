from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, date

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    tasks = db.relationship('Task', backref='user', lazy=True)
    habits = db.relationship('Habit', backref='user', lazy=True)
    scores = db.relationship('Score', backref='user', lazy=True)
    pomodoros = db.relationship('PomodoroSession', backref='user', lazy=True)
    logs = db.relationship('ActivityLog', backref='user', lazy=True)
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)
    recommendation_logs = db.relationship('RecommendationLog', backref='user', lazy=True)
    daily_stats = db.relationship('DailyStats', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)
    schedule_blocks = db.relationship('ScheduleBlock', backref='user', lazy=True)
    model_feedback = db.relationship('ModelFeedback', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)



class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    due_date = db.Column(db.DateTime(timezone=True))
    is_done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime(timezone=True))
    predicted_best_time = db.Column(db.String(10))
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    repeat = db.Column(db.String(20), default='none')



class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    target_frequency = db.Column(db.String(10))
    start_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    entries = db.relationship('HabitEntry', backref='habit', lazy=True)


class PomodoroSession(db.Model):
    __tablename__ = 'pomodoro_sessions'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Badge(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    condition = db.Column(db.String(255))


class UserBadge(db.Model):
    __tablename__ = 'user_badges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'))
    awarded_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity_type = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    meta_info = db.Column(db.JSON)


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    suggestion_type = db.Column(db.String(100))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RecommendationLog(db.Model):
    __tablename__ = 'recommendation_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recommended_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    recommendation_type = db.Column(db.String(50))
    recommendation_data = db.Column(db.JSON)
    accepted = db.Column(db.Boolean, default=False)


class DailyStats(db.Model):
    __tablename__ = 'daily_stats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    tasks_completed = db.Column(db.Integer, default=0)
    tasks_failed = db.Column(db.Integer, default=0)
    pomodoros_completed = db.Column(db.Integer, default=0)
    active_minutes = db.Column(db.Integer, default=0)
    focus_score = db.Column(db.Float, default=0.0)
    habit_success_rate = db.Column(db.Float, default=0.0)

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    goal_type = db.Column(db.String(50))
    target_date = db.Column(db.Date)
    target_value = db.Column(db.Float)
    current_value = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_completed = db.Column(db.Boolean, default=False)


class ScheduleBlock(db.Model):
    __tablename__ = 'schedule_blocks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    activity = db.Column(db.String(100))
    source = db.Column(db.String(50))


class ModelFeedback(db.Model):
    __tablename__ = 'model_feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model_type = db.Column(db.String(50))
    feedback = db.Column(db.String(500))
    submitted_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ModelPredictionLog(db.Model):
    __tablename__ = 'model_prediction_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model_type = db.Column(db.String(50))
    prediction = db.Column(db.String(500))
    input_features = db.Column(db.JSON)
    confidence_score = db.Column(db.Float)
    predicted_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    was_accepted = db.Column(db.Boolean)


class HabitEntry(db.Model):
    __tablename__ = 'habit_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'))
    date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)


class ModelVersion(db.Model):
    __tablename__ = 'model_versions'

    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String(50))
    version = db.Column(db.String(50))
    training_data_info = db.Column(db.JSON)
    accuracy = db.Column(db.Float)
    deployed_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(200))
    remind_at = db.Column(db.DateTime)
    sent = db.Column(db.Boolean, default=False)


class TimeLog(db.Model):
    __tablename__ = 'time_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)


class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    theme = db.Column(db.String(20))
    notifications_enabled = db.Column(db.Boolean, default=True)
    timezone = db.Column(db.String(50))






