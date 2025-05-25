from flask_sqlalchemy import SQLAlchemy
from flask import *
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")  # Fix for Render
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    roles = db.Column(db.JSON)  # Store as JSON (e.g., ["admin", "user"])

# Initialize tables (run once)
with app.app_context():
    db.create_all()