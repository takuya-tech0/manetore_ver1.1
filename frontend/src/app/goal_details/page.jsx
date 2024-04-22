"use client"; // これは Next.js 12 で必要な場合にのみ使用します。
import React, { useState, useEffect } from 'react';
import './goal_details.css';
import Link from 'next/link';

function Page() {
  const [data, setData] = useState({ item_name: '', remaining_amount: 0 });

  useEffect(() => {
    const fetchCustomers = async () => {
      const childUserId = 1;
      try {
        const res = await fetch(`http://127.0.0.1:5000/user_goal/${childUserId}`, { cache: "no-cache" });
        if (!res.ok) {
          throw new Error('Failed to fetch user goal');
        }
        const data = await res.json();
        setData(data);
      } catch (error) {
        console.error('Fetching data failed', error);
      }
    };
    fetchCustomers();
  }, []);

  return (
    <div className="page-container">
      {/* 画像コンテナ */}
      <div className="makeset-container">
        <img src="/image/makeset.png" alt="Makeup Set" className="makeset-image" />
      </div>

         {/* アイテム名と残金額 */}
         <div className="text-container">
        <div className="text-box">
          <p className="item-name">{data.item_name}まで</p>
          <p className="remaining-amount"><strong>￥</strong>{data.remaining_amount}</p>
        </div>
      </div>

 {/* salesboxコンテナ */}
 <div className="sale-box">
  <img src="/image/butalogo.png" alt="Logo" class="sale-logo" />
  <div class="sale-text">
    <p>コーヒーをうる</p>
    <p> 17かい</p>
  </div>
</div>

      {/* ボタンコンテナ */}
      <div className="button-container">
        <Link href="/grow" prefetch={false}>
          <button className="button button-grow">ふやす</button>
        </Link>
        <Link href="/purchase" prefetch={false}>
          <button className="button button-purchase">つかう</button>
        </Link>
      </div>
    </div>
  );
}

export default Page;