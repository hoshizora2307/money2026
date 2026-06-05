import streamlit as st
import datetime
import json
import os

# ==========================================
# 1. 完全ブラウザ制御・マトリックス起動システム（高視認性）
# ==========================================
st.set_page_config(page_title="返済管理システム Core", page_icon="🚀", layout="centered")

# CSS / JavaScript 一体型埋め込み（Python側でのスリープやrerunを排除）
matrix_boot_html = """
<style>
    /* --- マトリックス風スプラッシュ画面の設定 --- */
    #matrix-splash-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #000000;
        z-index: 999999;
        overflow: hidden;
        transition: opacity 0.6s ease-in-out, visibility 0.6s;
    }
    #matrixCanvas {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0.6;
    }
    .matrix-text {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%) scale(0.95);
        color: #ffffff;
        font-family: 'Noto Serif JP', 'Georgia', serif;
        font-size: calc(22px + 2vw);
        font-weight: bold;
        letter-spacing: 6px;
        white-space: nowrap;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
        opacity: 0;
        transition: all 0.5s ease-out;
    }

    /* --- メイン画面のベースデザイン --- */
    .stApp {
        background: radial-gradient(ellipse at bottom, #050c14 0%, #010205 100%) !important;
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        overflow-x: hidden;
    }

    /* 星空微細エフェクト */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px);
        background-size: 300px 300px; opacity: 0.15; z-index: 0; pointer-events: none;
    }

    /* タイトルエリア */
    .cyber-title-container {
        text-align: center; padding: 15px 10px; margin-bottom: 25px;
        background: rgba(2, 4, 10, 0.9); border: 2px solid #00ff41; border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2), inset 0 0 15px rgba(0, 255, 65, 0.1);
    }
    .cyber-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: calc(14px + 2.2vw) !important; color: #ffffff !important;
        text-shadow: 0 0 5px #00ff41, 0 0 10px #00ff41; letter-spacing: 1px; margin: 0 !important; white-space: nowrap;
    }
    .cyber-subtitle {
        font-size: calc(9px + 0.5vw); color: #00ffaa; text-shadow: 0 0 4px #00ffaa; letter-spacing: 2px; margin-top: 8px; white-space: nowrap;
    }
    .cyber-credit {
        font-size: calc(8px + 0.3vw); color: #888888; letter-spacing: 1px; margin-top: 10px; white-space: nowrap;
    }

    h3 {
        color: #00ffaa !important; text-shadow: 0 0 8px rgba(0,255,170,0.4); border-left: 4px solid #00ffaa;
        padding-left: 10px; font-size: calc(16px + 1vw) !important; white-space: nowrap;
    }
    
    div[data-testid="stMetricLabel"] { color: #ffffff !important; font-weight: bold !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important; }
    div[data-testid="stMetricValue"] { color: #00ff41 !important; font-size: 2.3rem !important; text-shadow: 0 0 10px rgba(0, 255, 65, 0.5); }

    /* ラジオボタンと文字の高視認性設定 */
    .stWidgetLabel, div[data-testid="stMarkdownContainer"] p, label, .stRadio p {
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 1), 0 0 2px rgba(0, 0, 0, 1) !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* ウィジェット外枠コンテナ */
    div[data-testid="stVerticalBlock"] {
        background: rgba(4, 8, 16, 0.85) !important; border-radius: 10px; padding: 12px;
        border: 1px solid rgba(0, 255, 65, 0.15);
    }
    .stAlert div { color: #ffffff !important; }
</style>

<div id="matrix-splash-container">
    <canvas id="matrixCanvas"></canvas>
    <div id="splash-msg" class="matrix-text">信頼に感謝</div>
</div>

<script>
    (function() {
        const container = document.getElementById('matrix-splash-container');
        const canvas = document.getElementById('matrixCanvas');
        const msg = document.getElementById('splash-msg');
        
        // すでにセッション内で閲覧済みの場合はオープニングをスキップ
        if (sessionStorage.getItem('matrix_auth_done')) {
            container.style.display = 'none';
            return;
        }

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const katakana = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        const alphabet = katakana.split("");
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const rainDrops = Array(Math.floor(columns)).fill(1);

        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00ff41';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet[Math.floor(Math.random() * alphabet.length)];
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        }

        const matrixInterval = setInterval(drawMatrix, 30);

        // 0.3秒後にメッセージをフェードイン＆拡張
        setTimeout(() => {
            msg.style.opacity = '1';
            msg.style.transform = 'translate(-50%, -50%) scale(1.05)';
            msg.style.letterSpacing = '10px';
        }, 300);

        // 2.2秒後にスプラッシュ全体をシャットダウン
        setTimeout(() => {
            clearInterval(matrixInterval);
            container.style.opacity = '0';
            container.style.visibility = 'hidden';
            sessionStorage.setItem('matrix_auth_done', 'true');
            setTimeout(() => { container.style.display = 'none'; }, 600);
        }, 2200);
    })();
</script>
"""

# HTML/JSコードを最上部で1回だけ確実に射出
st.markdown(matrix_boot_html, unsafe_allow_html=True)

# メインのタイトルヘッダー
st.markdown("""
<div class="cyber-title-container">
    <div class="cyber-title">⚡ 返済管理コアシステム ⚡</div>
    <div class="cyber-subtitle">SYSTEM VER 1.00 / 相互ロック制御</div>
    <div class="cyber-credit">BY HOSHIZORA2307 SOFTWARE SYSTEMS</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 2. データ管理ロジック
# ==========================================
DATA_FILE = "repayment_status.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "total_loan": 701000,
        "remaining_amount": 701000,
        "daichi_paid": False,
        "shizu_confirmed": False,
        "history": []
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = load_data()

db = st.session_state.db

# ==========================================
# 3. メインUIコンテンツ
# ==========================================
col1, col2 = st.columns(2)
with col1:
    st.metric(label="☄️ 元金（初期借入額）", value="¥701,000")
with col2:
    st.metric(label="🛰️ 現在の借入残高", value=f"¥{db['remaining_amount']:,}")

st.write("---")
st.subheader("🛸 今月の返済ステータス")

c1, c2 = st.columns(2)
with c1:
    if db["daichi_paid"]:
        st.success("🟢 だいち：返済シグナル送信済")
    else:
        st.warning("⚪ だいち：未返済")

with c2:
    if db["shizu_confirmed"]:
        st.success("🟢 しづ：受領確認サイン済")
    else:
        st.warning("⚪ しづ：未確認")

# ==========================================
# 4. 相互コントロールパネル
# ==========================================
st.write("---")
st.subheader("🎛️ コントロールパネル")

user_role = st.radio("アクセス権限を選択してください：", ["だいち (借主)", "しづ (貸主)"], horizontal=True)

if user_role == "だいち (借主)":
    st.info("💡 今月分の50,000円（＋利息）を振り込んだら、下のボタンを押してシグナルを送ってください。")
    if st.button("🚀 返済を実行した（シグナル送信）", disabled=db["daichi_paid"]):
        db["daichi_paid"] = True
        save_data(db)
        st.success("だいちの返済シグナルをロックしました。しづの承認を待ちます。")
        st.rerun()

elif user_role == "しづ (貸主)":
    st.info("💡 だいちからの入金を確認したら、下のボタンを押してトランザクションを確定させてください。")
    if not db["daichi_paid"]:
        st.error("⚠️ だいちからの返済シグナルがまだ送信されていません。")
    
    if st.button("🛸 着金を確認した（承認サイン）", disabled=(not db["daichi_paid"] or db["shizu_confirmed"])):
        db["shizu_confirmed"] = True
        
        repay_unit = 50000 
        db["remaining_amount"] = max(0, db["remaining_amount"] - repay_unit)
        
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        db["history"].append(f"{now_str} : ¥{repay_unit:,} の返済が承認されました。")
        
        db["daichi_paid"] = False
        db["shizu_confirmed"] = False
        
        save_data(db)
        st.success("トランザクション確定！残高が更新され、ログが記録されました。")
        st.rerun()

# ==========================================
# 5. ログ・タイムライン履歴
# ==========================================
st.write("---")
st.subheader("📜 分割返済の履歴データ")
if db["history"]:
    for record in reversed(db["history"]):
        st.code(record, language="markdown")
else:
    st.caption("通信記録なし（承認された返済履歴はまだありません）")
