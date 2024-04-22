import Link from 'next/link';
import styles from './page.module.css'; // CSSモジュールをインポート

export default function Home() {
  // 背景スタイルオブジェクト
  const backgroundStyle = {
    background: "url('/image/backimage.png') no-repeat center center fixed",
    backgroundSize: 'cover',
    minWidth: '432px',
    minHeight: '932px',
  };

  return (
    // 背景スタイルを適用したdivタグで全体をラップ
    <div style={backgroundStyle}>
      <div className={styles.container}> 
        {/* ロゴの画像 */}
        <img src="/image/manetorelogo.png" alt="マネトレロゴ" className={styles.logo} />
      
        {/* ユーザーネーム入力フィールド */}
        <div>
          <label htmlFor="username">なまえ:</label>
          <input id="username" type="text" name="username" required className={styles.inputField} />
        </div>

        {/* パスワード入力フィールド */}
        <div>
          <label htmlFor="password">ばんごう:</label>
          <input id="password" type="password" name="password" required className={styles.inputField} />
        </div>

        {/* ログインボタン */}
        <Link href="/login" passHref>
          <button type="button" className={styles.loginButton}>ログイン</button>
        </Link>
      </div>
    </div>  
  );
}
