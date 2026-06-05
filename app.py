import streamlit as st
import datetime
import json
import os

# ==========================================
# 1. 宇宙背景の完全復活 ＆ マトリックス・サイバーCSS
# ==========================================
st.set_page_config(page_title="返済管理システム Core", page_icon="🚀", layout="centered")

cyber_matrix_space_html = """
<style>
    /* --- 1. 元の美しい宇宙・スペース背景の完全復活 --- */
    .stApp {
        /* 深宇宙のディープブルーグラデーション */
        background: radial-gradient(ellipse at center, #0a1128 0%, #020617 100%) !important;
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        overflow-x: hidden;
    }

    /* 微細な星空エフェクトの複写 */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 40px),
            radial-gradient(rgba(255,255,255,0.15), rgba(255,255,255,0.05) 1px, transparent 30px);
        background-size: 350px 350px, 200px 200px; 
        opacity: 0.25; 
        z-index: 0; 
        pointer-events: none;
    }

    /* --- 2. メッセージがマトリックス風に流れる起動演出（上部マトリックス・バナー） --- */
    @keyframes matrix-stream-fade {
        0% { opacity: 0; transform: scaleY(0); }
        15% { opacity: 1; transform: scaleY(1); }
        85% { opacity: 1; transform: scaleY(1); }
        100% { opacity: 0; transform: scaleY(0); height: 0; margin-bottom: 0; padding: 0; visibility: hidden; }
    }
    @keyframes code-rain-scroll {
        0% { background-position: 0% 0%; }
        100% { background-position: 0% 100%; }
    }
    @keyframes message-glow {
        0% { opacity: 0; letter-spacing: 4px; filter: blur(2px); }
        20% { opacity: 1; letter-spacing: 8px; filter: blur(0px); text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41; }
        80% { opacity: 1; letter-spacing: 10px; text-shadow: 0 0 12px #00ff41, 0 0 25px #00ff41; }
        100% { opacity: 0; filter: blur(2px); }
    }

    /* 上部にマトリックスデジタル空間をコンパクトに展開 */
    .matrix-top-booter {
        position: relative;
        width: 100%;
        height: 100px;
        background-color: rgba(0, 0, 0, 0.85);
        border: 1px solid #00ff41;
        border-radius: 6px;
        margin-bottom: 20px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: matrix-stream-fade 3.5s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;
    }
    
    /* マトリックスコード雨のデジタル背景（CSS高速スクロール） */
    .matrix-top-booter::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-image: linear-gradient(180deg, rgba(0, 255, 65, 0.2) 0%, transparent 80%);
        background-size: 100% 50px;
        opacity: 0.7;
        animation: code-rain-scroll 1s linear infinite;
    }

    /* 「信頼に感謝」のメッセージ発光 */
    .matrix-boot-message {
        position: relative;
        color: #ffffff;
        font-family: 'Noto Serif JP', 'Georgia', serif;
        font-size: calc(18px + 1vw);
        font-weight: bold;
        white-space: nowrap;
        z-index: 10;
        animation: message-glow 3.2s ease-in-out forwards;
    }

    /* --- 3. メインUIコンポーネントのサイバーデザイン --- */
    .cyber-title-container {
        text-align: center; padding: 18px 10px; margin-bottom: 25px; position: relative;
        background: rgba(4, 10, 24, 0.85); border: 2px solid #00ffaa; border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.25), inset 0 0 15px rgba(0, 255, 170, 0.1);
    }
    .cyber-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: calc(15px + 2vw) !important; color: #ffffff !important;
        text-shadow: 0 0 5px #00ffaa, 0 0 12px #00ffaa; letter-spacing: 2px; margin: 0 !important; white-space: nowrap;
    }
    .cyber-subtitle {
        font-size: calc(9px + 0.4vw); color: #00ff41; text-shadow: 0 0 4px #00ff41; letter-spacing: 2px; margin-top: 8px; white-space: nowrap;
    }
    .cyber-credit {
        font-size: calc(7px + 0.3vw); color: #888888; letter-spacing: 1px; margin-top: 10px; white-space: nowrap;
    }

    h3 {
        color: #00ffaa !important; text-shadow: 0 0 8px rgba(0,255,170,0.4); border-left: 4px solid #00ffaa;
        padding-left: 10px; font-size: calc(15px + 0.8vw) !important; white-space: nowrap;
    }
    
    div[data-testid="stMetricLabel"] { color: #ffffff !important; font-weight: bold !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important; }
    div[data-testid="stMetricValue"] { color: #00ffaa !important; font-size: 2.2rem !important; text-shadow: 0 0 10px rgba(0, 255, 170, 0.4); }

    .stWidgetLabel, div[data-testid="stMarkdownContainer"] p, label, .stRadio p {
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 1) !important;
        font-weight: 600 !important;
    }

    /* ウィジェット外枠コンテナ（透明感のあるサイバーネイビー） */
    div[data-testid="stVerticalBlock"] {
        background: rgba(5, 12, 28, 0.75) !important; border-radius: 10px; padding: 14px;
        border: 1px solid rgba(0, 255, 170, 0.2);
    }
    .stAlert div { color: #ffffff !important; }
</style>

<div class="matrix-top-booter">
    <div class="matrix-boot-message">信頼に感謝</div>
</div>
"""

# スタイリングと起動メッセージの射出
st.markdown(cyber_matrix_space_html, unsafe_allow_html=True)

# メインタイトル
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
