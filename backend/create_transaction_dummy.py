from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TransactionTable(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    in_out_flag = db.Column(db.Integer, nullable=False)  # 入金か出金のフラグ
    amount = db.Column(db.Float, nullable=False)
    transaction_type_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)

def insert_dummy_data():
    # 画像をバイナリデータとして読み込む関数
    def load_image_binary(filepath):
        with open(filepath, "rb") as image_file:
            return image_file.read()

    # チョコレートのダミーデータ
    dummy_data = TransactionTable(
        child_user_id=1,
        in_out_flag=1,
        amount=108.0,
        transaction_type_id=1,
        content='チョコレート',
        image=load_image_binary('frontend/image/chocolate.jpg')
    )
    # ゼリーのダミーデータ
    dummy_data2 = TransactionTable(
        child_user_id=1,
        in_out_flag=1,
        amount=110.0,
        transaction_type_id=1,
        content='ゼリー',
        image=load_image_binary('frontend/image/jelly.jpg')
    )
    # シールブックのダミーデータ
    dummy_data3 = TransactionTable(
        child_user_id=1,
        in_out_flag=1,
        amount=110.0,
        transaction_type_id=1,
        content='シールブック',
        image=load_image_binary('frontend/image/sealbook.jpg')
    )
    # お菓子のダミーデータ
    dummy_data4 = TransactionTable(
        child_user_id=1,
        in_out_flag=1,
        amount=110.0,
        transaction_type_id=1,
        content='お菓子',
        image=load_image_binary('frontend/image/Dagashi.jpg')
    )

    # 全てのダミーデータをデータベースセッションに追加
    db.session.add(dummy_data)
    db.session.add(dummy_data2)
    db.session.add(dummy_data3)
    db.session.add(dummy_data4)
    db.session.commit()

with app.app_context():
    db.create_all()  # データベーステーブルを作成します。
    insert_dummy_data()  # ダミーデータを挿入します。
