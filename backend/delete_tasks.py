import sys
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TaskTable(db.Model):
    __tablename__ = 'task_table'
    task_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())
    person = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)
    resolve = db.Column(db.String, nullable=True)
    amount = db.Column(db.Float, nullable=False)

def delete_task(task_id):
    with app.app_context():
        task = TaskTable.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            print(f"タスクID {task_id} のデータが削除されました。")
        else:
            print(f"タスクID {task_id} のデータが見つかりませんでした。")

if __name__ == '__main__':
    task_id_to_delete = 2  # 削除したいタスクIDをここに指定
    delete_task(task_id_to_delete)
