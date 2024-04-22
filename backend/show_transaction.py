# show_transactions.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TransactionTable(db.Model):
    __tablename__ = 'transaction_table'
    transaction_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, db.ForeignKey('users.child_user_id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    in_out_flag = db.Column(db.Integer, nullable=False)  # 入金か出金のフラグ
    amount = db.Column(db.Float, nullable=False)
    transaction_type_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)

def show_transactions():
    with app.app_context():
        transactions = TransactionTable.query.all()
        for transaction in transactions:
            # print(f"Transaction ID: {transaction.transaction_id}")
            # print(f"Child User ID: {transaction.child_user_id}")
            # print(f"Created Date: {transaction.created_date}")
            # print(f"In/Out Flag: {'入金' if transaction.in_out_flag == 1 else '出金'}")
            # print(f"Amount: {transaction.amount}")
            # print(f"Transaction Type ID: {transaction.transaction_type_id}")
            # print(f"Content: {transaction.content}")
            print(f"Image URL: {transaction.image if transaction.image else 'No image'}")
            # print("-" * 40)

if __name__ == '__main__':
    show_transactions()
