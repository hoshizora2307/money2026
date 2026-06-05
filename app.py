import streamlit as st
import datetime
import json
import os

# ==========================================
# 1. 宇宙ベース(星空・流星・オービット惑星)カスタムCSS/HTML
# ==========================================
st.set_page_config(page_title="SpaceLab Repayment Core", page_icon="🚀", layout="centered")

space_effects_html = """
<style>
    /* 全体の背景を深い宇宙に設定 */
    .stApp {
        background: radial-gradient(ellipse at bottom, #0c1020 0%, #030308 100%) !important;
        color: #e0e0ff;
        font-family: 'Courier New', Courier, monospace;
        overflow-x: hidden;
    }

    /* リアルな星空を生成する背景レイヤー */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px);
        background-size: 550px 550px, 350px 350px, 250px 250px;
        background-position: 0 0, 40px 60px, 130px 270px;
        opacity: 0.3;
        z-index: 0;
        pointer-events: none;
    }

    /* 流れ星のアニメーション */
    @keyframes shooting-star {
        0% { transform: translateX(0) translateY(0) rotate(-45deg) scale(0); opacity: 0; }
        5% { opacity: 1; transform: translateX(-100px) translateY(100px) rotate(-45deg) scale(1); }
        15% { transform: translateX(-400px) translateY(400px) rotate(-45deg) scale(0); opacity: 0; }
        100% { transform: translateX(-400px) translateY(400px) rotate(-45deg) scale(0); opacity: 0; }
    }
    .stApp::after {
        content: "";
        position: fixed;
        top: 15%; right: -10%; width: 140px; height: 2px;
        background: linear-gradient(-45deg, #00ffff, rgba(0, 0, 0, 0));
        filter: drop-shadow(0 0 6px #00ffff);
        opacity: 0;
        animation: shooting-star 12s linear infinite;
        z-index: 0;
        pointer-events: none;
    }

    /* --- 太陽系惑星オービットシステム (背景アニメーション) --- */
    @keyframes orbit-rotate {
        from { transform: translate(-50%, -50%) rotate(0deg); }
        to { transform: translate(-50%, -50%) rotate(360deg); }
    }

    /* 惑星配置用の固定コンテナ */
    .solar-system {
        position: fixed;
        top: 50%;
        left: 50%;
        width: 0px;
        height: 0px;
        z-index: 0;
        pointer-events: none;
        opacity: 0.25;
    }

    /* 中心：太陽光（バックグロー） */
    .sun-glow {
        position: absolute;
        width: 100px; height: 100px;
        background: radial-gradient(circle, rgba(255,150,0,0.3) 0%, transparent 70%);
        transform: translate(-50%, -50%);
    }

    /* 軌道と惑星の共通定義 */
    .orbit {
        position: absolute;
        border: 1px dashed rgba(0, 255, 255, 0.15);
        border-radius: 50%;
        animation: orbit-rotate linear infinite;
    }
    .planet {
        position: absolute;
        top: 0;
        left: 50%;
        border-radius: 50%;
        transform: translate(-50%, -50%);
    }

    /* 内側惑星（地球イメージ・青） */
    .orbit-inner {
        width: 280px; height: 280px;
        animation-duration: 25s;
    }
    .planet-inner {
        width: 10px; height: 10px;
        background: #00bfff;
        box-shadow: 0 0 8px #00bfff;
    }

    /* 外側惑星（土星・環つきイメージ・オレンジ） */
    .orbit-outer {
        width: 520px; height: 520px;
        animation-duration: 50s;
    }
    .planet-outer {
        width: 16px; height: 16px;
        background: #ffaa44;
        box-shadow: 0 0 10px #ffaa44;
    }
    .planet-outer::after {
        content: "";
        position: absolute;
        top: 50%; left: 50%;
        width: 26px; height: 6px;
        border: 2px solid rgba(255, 170, 68, 0.6);
        border-radius: 50%;
        transform: translate(-50%, -50%) rotate(15deg);
    }

    /* --- UIデザインの強化 --- */
    .cyber-title-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 25px;
        background: rgba(5, 5, 20, 0.7);
        border: 2px solid #00ffff;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3), inset 0 0 15px rgba(0, 255, 255, 0.2);
    }
    .cyber-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: 24pt !important;
        color: #ffffff !important;
        text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff, 0 0 20px #00ffff;
        letter-spacing: 4px;
        margin: 0 !important;
    }
    .cyber-subtitle {
        font-size: 9pt; color: #ff00ff;
        text-shadow: 0 0 4px #ff00ff; letter-spacing: 6px; margin-top: 5px;
    }
    .cyber-credit {
        font-size: 8pt; color: #00ffaa;
        text-shadow: 0 0 3px #00ffaa; letter-spacing: 2px; margin-top: 10px;
    }
    h3 { color: #ff00ff !important; text-shadow: 0 0 8px #ff00ff; border-left: 4px solid #ff00ff; padding-left: 10px; }
    div[data-testid="stMetricValue"] { color: #00ffaa !important; font-size: 2.3rem !important; text-shadow: 0 0 10px rgba(0, 255, 170, 0.6); }
    
    /* コンテンツの視認性を確保するためのレイヤー調整 */
    div[data-testid="stVerticalBlock"] {
        background: rgba(4, 5, 15, 0.4);
        border-radius: 10px;
        padding: 10px;
    }
</style>

<div class="solar-system">
    <div class="sun-glow"></div>
    <div class="orbit orbit-inner">
        <div class="planet planet-inner"></div>
    </div>
    <div class="orbit orbit-outer">
        <div class="planet planet-outer"></div>
    </div>
</div>

<div class="cyber-title-container">
    <div class="cyber-title">⚡ REPAYMENT CORE ⚡</div>
    <div class="cyber-subtitle">SYSTEM VER 2.06 / SPICELAB NAVIGATION</div>
    <div class="cyber-credit">BY HOSHIZORA2307 SOFTWARE SYSTEMS</div>
</div>
"""
st.markdown(space_effects_html, unsafe_allow_html=True)

# ==========================================
# 2. データ管理ロジック (構文エラー修正済)
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
    st.metric(label="☄️ INITIAL LOAN", value="¥701,000")
with col2:
    st.metric(label="🛰️ CURRENT REMAINING", value=f"¥{db['remaining_amount']:,}")

st.write("---")
st.subheader("🛸 Current Cycle Status")

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
st.subheader("🎛️ Mission Control Panel")

user_role = st.radio("アクセス権限を選択してください：", ["小野田 だいち (借主)", "川端 しづ (貸主)"], horizontal=True)

if user_role == "小野田 だいち (借主)":
    st.info("💡 今月分の50,000円（＋利息）を振り込んだら、下のボタンを押してシグナルを送ってください。")
    if st.button("🚀 返済を実行した（シグナル送信）", disabled=db["daichi_paid"]):
        db["daichi_paid"] = True
        save_data(db)
        st.success("だいちさんからの返済シグナルをロックしました。しづさんの承認を待ちます。")
        st.rerun()

elif user_role == "川端 しづ (貸主)":
    st.info("💡 だいちさんからの入金を確認したら、下のボタンを押してトランザクションを確定させてください。")
    if not db["daichi_paid"]:
        st.error("⚠️ だいちさんからの返済シグナルがまだ送信されていません。")
    
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
st.subheader("📜 Quantum Ledger (返済履歴)")
if db["history"]:
    for record in reversed(db["history"]):
        st.code(record, language="markdown")
else:
    st.caption("通信記録なし（まだ承認された返済はありません）")
