# drop_task_table.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TaskTable(db.Model):
    __tablename__ = 'task_table'
    task_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime)
    person = db.Column(db.String)
    content = db.Column(db.String)
    resolve = db.Column(db.String)
    amount = db.Column(db.Float)
    image = db.Column(db.Text)

def drop_table():
    with app.app_context():
        # 特定のテーブルを削除
        TaskTable.__table__.drop(db.engine)

if __name__ == '__main__':
    drop_table()
