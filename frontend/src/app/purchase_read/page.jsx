// page.jsx
"use client";
import React, { useState, useEffect } from 'react';
import Link from 'next/link';

function Page() {
  const [transactions, setTransactions] = useState([]); // 初期値を空の配列に設定

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/purchase_read/1`);
        const data = await response.json();
        if (Array.isArray(data)) { // データが配列であることを確認
          setTransactions(data);
        } else {
          throw new Error('Data is not an array');
        }
      } catch (error) {
        console.error('Fetching transactions failed', error);
      }
    };
    fetchTransactions();
  }, []);

  return (
    <div>
      <h1>購入履歴</h1>
      {transactions.map(transaction => ( // transactions 配列の各要素に対してカードを生成
        <div key={transaction.transaction_id} className="m-4 card bordered bg-blue-200 duration-200 hover:border-r-red">
          <div className="card-body">
            <p>{transaction.content}</p>
            <p>{transaction.amount}円</p>
            {transaction.image && <img src={`data:image/png;base64,${transaction.image}`} alt="Transaction Image" />}
            <div className="button-container">
              <button className="button">変更</button>
              <button className="button">完了</button>
            </div>
          </div>
        </div>
      ))}
      <div className="navigation-buttons">
        <Link href="/previous"><button className="button">戻る</button></Link>
        <Link href="/next"><button className="button">進む</button></Link>
      </div>
    </div>
  );
}

export default Page;
