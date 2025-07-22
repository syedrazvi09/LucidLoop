from flask import Flask
from flask_migrate import Migrate
from models import db
from dashboard import bp  # bp, not dashboard

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)

print("This is in Development, and testing phase")