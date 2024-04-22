"use client";
import React, { useState, useEffect } from 'react';
import './purchase.css';
import Link from 'next/link'

function Page() {
  const [formInput, setFormInput] = useState({
    content: '',
    amount: '',
    category: ''
  });
  const [file, setFile] = useState(null); // 画像ファイルの状態

  // page.jsxのhandleSubmit関数を以下のように編集
  const handleSubmit = async (e) => {
    console.log('handleSubmit called'); // この行を追加
    e.preventDefault(); // フォームのデフォルト送信を防止

    // JSON形式でデータを準備
    const jsonData = {
      content: formInput.content,
      amount: parseFloat(formInput.amount), // 文字列から数値へ変換
      image: 'test', // 固定値
      child_user_id: 1, // 固定値
      in_out_flag: 1, // 固定値
      transaction_type_id: 2, // 固定値
    };

    // APIエンドポイントへのPOSTリクエスト
    const response = await fetch('http://127.0.0.1:5000/purchase/1', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jsonData),
    });

    if (response.ok) {
      console.log('Transaction created successfully');
      // 追加の処理（成功メッセージの表示など）
    } else {
      console.error('Failed to create transaction');
      // エラー処理
    }
  };

  // 入力フィールドとファイルの変更を処理
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormInput({ ...formInput, [name]: value });
  };

  // ファイル入力の変更を処理
  const handleFileChange = (e) => {
    setFile(e.target.files[0]); // 選択されたファイルを状態にセット
  };

  return (
    <div className="form-container">
      <div className="title-container"> {/* タイトルセクション */}
        <h1 className="form-title">つかう</h1>
      </div>

      <div className="fields-container"> {/* 入力フィールドセクション */}
        <form onSubmit={handleSubmit} className="form-content">
          <div className="field-box">
            <label className="form-label">ないよう</label>
            <input
              className="form-input"
              type="text"
              name="content"
              value={formInput.content}
              onChange={handleChange}
            />
          </div>

          <div className="field-box">
            <label className="form-label">きんがく</label>
            <input
              className="form-input"
              type="number"
              name="amount"
              value={formInput.amount}
              onChange={handleChange}
            />
          </div>
          <div className="field-box">
            <label className="form-label">がぞう</label>
            <input
              className="form-file-input"
              type="file"
              name="purchase_image"
              onChange={handleFileChange}
            />
          </div>

          <div className="registration-section">
  <label className="registration-label">とうろく</label>
  <input
    type="checkbox"
    className="registration-checkbox"
    id="registration"
    name="registration"
  />
</div>

        </form>
      </div>
    
    
      <div className="buttons-container"> {/* ボタンセクション */}
        <button className="back-button" onClick={() => router.push('/goal_details')}>🔙もどる</button>
        <button className="form-submit-button" type="submit">かんりょう☑</button>
      </div>
    </div>
  );
}
export default Page;