from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    child_user_id = db.Column(db.Integer, primary_key=True)
    child_user_name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    initial_amount = db.Column(db.Float, nullable=False)
    pocket_money = db.Column(db.Float, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    money_left = db.Column(db.Float, nullable=False)

class Goal_information(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    item_name = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_reference_picture_url = db.Column(db.String)
    item_url = db.Column(db.String)
    child_user_id = db.Column(db.Integer, db.ForeignKey('users.child_user_id'))

def insert_dummy_data():
    user = Users(
        child_user_id=1,
        child_user_name='サンプル太郎',
        birth_date=datetime(2000, 1, 1),
        initial_amount=500,
        pocket_money=330,
        update_time=datetime(2024, 3, 1),
        money_left=500
    )

    goal = Goal_information(
        goal_id=1,
        created_date=datetime(2024, 3, 1),
        item_name='メイクセット',
        item_price=1000,
        item_reference_picture_url='sample',
        item_url='sample',
        child_user_id=1
    )

    db.session.add(user)
    db.session.add(goal)
    db.session.commit()

with app.app_context():
    db.create_all()  # データベーステーブルを作成します。
    insert_dummy_data()  # ダミーデータを挿入します。
