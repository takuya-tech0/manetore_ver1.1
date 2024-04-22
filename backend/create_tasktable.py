# create_tasktable.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TaskTable(db.Model):
    __tablename__ = 'task_table'
    task_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    person = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)
    resolve = db.Column(db.String, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=True)

def insert_dummy_data():
    with open("/Users/takuya/Desktop/manetore/frontend/image/grow_mother.png", "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    dummy_data = TaskTable(
        child_user_id=1,
        person="ママ",
        content='あさのじゅんびがたいへん',
        resolve='コーヒーをうる',
        amount=30,
        image=img_data
    )
    db.session.add(dummy_data)
    db.session.commit()

with app.app_context():
    db.create_all()
    insert_dummy_data()
