from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TaskTable(db.Model):
    __tablename__ = 'task_table'
    task_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, db.ForeignKey('users.child_user_id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    person = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)
    resolve = db.Column(db.String, nullable=True)
    amount = db.Column(db.Float, nullable=False)

def show_tasks():
    with app.app_context():
        tasks = TaskTable.query.all()
        for task in tasks:
            print(f"Task ID: {task.task_id}")
            print(f"Child User ID: {task.child_user_id}")
            print(f"Created Date: {task.created_date}")
            print(f"Person: {task.person}")
            print(f"Content: {task.content}")
            print(f"Resolve: {task.resolve}")
            print(f"Amount: {task.amount}")
            print("-" * 40)

if __name__ == '__main__':
    show_tasks()
