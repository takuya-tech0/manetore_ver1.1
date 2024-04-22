# delete_transactions.py
import sys
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manetore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TransactionTable(db.Model):
    __tablename__ = 'transaction_table'
    transaction_id = db.Column(db.Integer, primary_key=True)
    child_user_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.now())
    in_out_flag = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)

def delete_transaction(transaction_id):
    with app.app_context():
        transaction = TransactionTable.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            print(f"トランザクションID {transaction_id} のデータが削除されました。")
        else:
            print(f"トランザクションID {transaction_id} のデータが見つかりませんでした。")

if __name__ == '__main__':
    transaction_id_to_delete = 6  # 削除したいトランザクションIDをここに指定
    delete_transaction(transaction_id_to_delete)
