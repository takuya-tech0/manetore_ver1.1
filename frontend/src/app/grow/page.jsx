// page.jsx
"use client";
import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // React Router v5の場合
import Link from 'next/link';

function Page() {
  const [tasks, setTasks] = useState([]);
  const history = useHistory(); // ナビゲーション用のフックを追加

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/grow_read/1`);
        const data = await response.json();
        if (Array.isArray(data)) {
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

  const handleCompleteTask = async (task) => {
    const jsonData = {
      content: task.resolve,
      amount: task.amount,
      image: task.image,
      child_user_id: 1, // 例として固定値
      in_out_flag: 2, // 入金を示す
      transaction_type_id: 2 // 固定のトランザクションタイプID
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/grow/1', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData)
      });
      if (!response.ok) throw new Error('Failed to create transaction');
      const result = await response.json();
      console.log('Transaction created successfully:', result);
      history.push('/goal_details'); // トランザクション成功後にページ遷移
    } catch (error) {
      console.error('Failed to complete task', error);
    }
  };

  return (
    <div>
      <h1>ふやす</h1>
      {tasks.map(task => (
        <div key={task.task_id} className="m-4 card bordered bg-blue-200 duration-200 hover:border-r-red">
          <div className="card-body">
            <p>{task.resolve}</p>
            <p>{task.amount}えん/1かい</p>
            {task.image && <img src={`data:image/png;base64,${task.image}`} alt="Task Image" />}
            <div className="button-container">
              <button className="button" onClick={() => handleCompleteTask(task)}>できた</button>
            </div>
          </div>
        </div>
      ))}
      <div className="navigation-buttons">
        <Link href="/previous"><button className="button">もどる</button></Link>
        <Link href="/next"><button className="button">すすむ</button></Link>
      </div>
    </div>
  );
}

export default Page;
