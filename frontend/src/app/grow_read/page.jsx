// page.jsx
"use client";
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import './grow_read.css'

function Page() {
  const [tasks, setTasks] = useState([]); // 初期値を空の配列に設定
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/grow_read/1`);
        const data = await response.json();
        if (Array.isArray(data)) { // データが配列であることを確認
          setTasks(data);
        } else {
          throw new Error('Data is not an array');
        }
      } catch (error) {
        console.error('Fetching tasks failed', error);
      }
    };
    fetchTasks();
  }, []);

  return (
    <div className="form-container">
      <div className="title-container"> {/* タイトルセクション */}
        <h1 className="form-title">ふやす</h1>
      </div>
  
      {tasks.map(task => ( // tasks 配列の各要素に対してカードを生成
        <div key={task.task_id} className="card">
          <div className="card-content"> {/* テキストと画像を横に並べるコンテナ */}
            <div>
              <p>{task.resolve}</p> {/* タスク名 */}
              <p>{task.amount}えん/1かい</p> {/* 金額 */}
            </div>
            {task.image && <img src={`data:image/png;base64,${task.image}`} alt="Task Image" />} {/* 画像 */}
          </div>
          <div className="button-container"> {/* ボタンのコンテナ */}
            <button className="button1">へんこう</button> {/* へんこうボタン */}
            <button className="button2">できた☑</button> {/* できたボタン */}
          </div>
        </div>
          ))}
          
      <div className="buttons-container"> {/* ボタンセクション */}
        <button className="back-button" onClick={() => router.push('/goal_details')}>🔙もどる</button>
        <button className="form-submit-button" type="submit">すすむ☑</button>
      </div>

    </div>
  );
}

export default Page;