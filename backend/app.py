# app.py
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import base64

# JWT認証のためのライブラリを追加
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# アプリケーションの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# JWTの秘密鍵を設定 (実際にはもっと安全な方法で管理する)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'


# SQLAlchemy インスタンスの初期化
db = SQLAlchemy(app)
# JWTマネージャーの初期化
jwt = JWTManager(app)

# 仮のユーザーデータとして「じゅり」の情報を追加 (生年月日とお小遣いを含む)
users = {
    "juri": {
        "password_hash": generate_password_hash('1111'),  # パスワードをハッシュ化して保存
        "name": "じゅり",
        "birth_date": "2020-07-07",
        "pocket_money": 330
    }
}

# ログイン機能のエンドポイントを修正
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = Users.query.filter_by(child_user_name=username).first()

    if user and check_password_hash(user.password_hash, password):
        # 認証成功時の処理
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        # 認証失敗時の処理
        return jsonify({"msg": "ユーザー名またはパスワードが間違っています"}), 401

# モデルの定義
class Users(db.Model):
    __tablename__ = 'users'
    child_user_id = db.Column(db.Integer, primary_key=True)
    child_user_name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    initial_amount = db.Column(db.Float, nullable=False)
    pocket_money = db.Column(db.Float, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    money_left = db.Column(db.Float, nullable=False)

class Goal_information(db.Model):
    __tablename__ = 'goal_information'
    goal_id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    item_name = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_reference_picture_url = db.Column(db.String)
    item_url = db.Column(db.String)
    child_user_id = db.Column(db.Integer, db.ForeignKey('users.child_user_id'))

class TransactionTable(db.Model):
    __tablename__ = 'transaction_table'
    transaction_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, db.ForeignKey('users.child_user_id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    in_out_flag = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)  # データ型をStringからLargeBinaryに変更

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

# アプリケーションのルートとビジネスロジック
@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/user_goal/1', methods=['GET'])
def get_user_goal():
    user = Users.query.filter_by(child_user_id=1).first()
    goal = Goal_information.query.filter_by(child_user_id=1).first()

    if not user or not goal:
        return jsonify({'error': 'User or Goal not found'}), 404

    remaining_amount = goal.item_price - user.money_left

    return jsonify({
        'item_name': goal.item_name,
        'remaining_amount': remaining_amount
    })

@app.route('/purchase/1', methods=['POST'])
def create_transaction_purchase():
    data = request.json
    new_transaction = TransactionTable(
        child_user_id=data['child_user_id'],
        created_date=datetime.utcnow(),
        in_out_flag=1,  # 1 は出金を示す
        amount=data['amount'],
        transaction_type_id=data['transaction_type_id'],
        content=data['content'],
        image=data['image']
    )
    db.session.add(new_transaction)

    user = Users.query.get(data['child_user_id'])
    if user:
        user.money_left -= data['amount']
        db.session.commit()
        return jsonify({'message': 'Transaction created and user updated successfully'}), 200
    else:
        db.session.rollback()
        return jsonify({'message': 'User not found'}), 404

@app.route('/grow/1', methods=['POST'])
def create_transaction_grow():
    data = request.json
    new_transaction = TransactionTable(
        child_user_id=data['child_user_id'],
        created_date=datetime.utcnow(),
        in_out_flag=2,  # 2 は入金を示す
        amount=data['amount'],
        transaction_type_id=data['transaction_type_id'],
        content=data['content'],
        image=data['image']
    )
    db.session.add(new_transaction)

    user = Users.query.get(data['child_user_id'])
    if user:
        user.money_left += data['amount']
        db.session.commit()
        return jsonify({'message': 'Transaction created and user updated successfully'}), 200
    else:
        db.session.rollback()
        return jsonify({'message': 'User not found'}), 404

@app.route('/grow_task_add/1', methods=['POST'])
def add_grow_task():
    # リクエストからデータを取得
    data = request.json
    # 新しいタスクを作成
    new_task = TaskTable(
        child_user_id=1,  # この例では固定値を使用
        created_date=datetime.utcnow(),
        person=data.get('person'),
        content=data.get('content'),
        resolve=data.get('resolve'),
        amount=data.get('amount')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'New grow task added successfully'}), 201

@app.route('/grow_read/1', methods=['GET'])
def read_tasks():
    tasks = TaskTable.query.filter_by(child_user_id=1).all()  # すべてのタスクを取得
    tasks_data = [{
        'task_id': task.task_id,
        'person': task.person,
        'content': task.content,
        'resolve': task.resolve,
        'amount': task.amount,
        'created_date': task.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        'image': task.image
    } for task in tasks]
    return jsonify(tasks_data)  # リスト形式でJSONデータを返す

@app.route('/purchase_read/1', methods=['GET'])
def read_transactions():
    transactions = TransactionTable.query.filter_by(transaction_type_id=1).all()
    transactions_data = [{
        'transaction_id': transaction.transaction_id,
        'child_user_id': transaction.child_user_id,
        'created_date': transaction.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        'in_out_flag': transaction.in_out_flag,
        'amount': transaction.amount,
        'transaction_type_id': transaction.transaction_type_id,
        'content': transaction.content,
        'image': base64.b64encode(transaction.image).decode('utf-8') if transaction.image else None
    } for transaction in transactions]
    return jsonify(transactions_data)

if __name__ == '__main__':
    app.run(debug=True)
