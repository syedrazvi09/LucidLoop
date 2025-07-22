from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)

print("This is in Development, and testing phase")
