import streamlit as st
import datetime
import json
import os
import time

# ==========================================
# 1. 宇宙ベース(高視認性サイバー)カスタムCSS/HTML
# ==========================================
st.set_page_config(page_title="返済管理システム Core", page_icon="🚀", layout="centered")

# ローカルまたはGitHub上の画像ファイル名
IMAGE_FILE = "f1293694-2ea8-4e0d-b55d-9af1a07146e5-1_all_7174.jpg"

space_effects_html = f"""
<style>
    /* --- オープニング画面（スプラッシュ）の定義 --- */
    @keyframes fade-in-out {{
        0% {{ opacity: 0; visibility: visible; }}
        15% {{ opacity: 1; }}
        85% {{ opacity: 1; }}
        100% {{ opacity: 0; visibility: hidden; }}
    }}
    @keyframes text-glow {{
        0% {{ opacity: 0; transform: translate(-50%, -40%); filter: blur(5px); }}
        30% {{ opacity: 1; transform: translate(-50%, -50%); filter: blur(0px); text-shadow: 0 0 10px #ffffff, 0 0 20px #ff00ff; }}
        100% {{ opacity: 1; transform: translate(-50%, -50%); text-shadow: 0 0 15px #ffffff, 0 0 30px #ff00ff; }}
    }}

    .splash-container {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #030308;
        background-image: url('{IMAGE_FILE}');
        background-size: cover;
        background-position: center;
        z-index: 99999;
        animation: fade-in-out 2.5s ease-in-out forwards;
        pointer-events: none;
    }}
    .splash-overlay {{
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle, rgba(3,3,8,0.2) 0%, rgba(3,3,8,0.7) 100%);
    }}
    .splash-text {{
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        color: #ffffff;
        font-family: 'Noto Serif JP', 'Georgia', serif;
        font-size: calc(20px + 2vw);
        font-weight: bold;
        letter-spacing: 8px;
        white-space: nowrap;
        animation: text-glow 2s ease-out forwards;
    }}

    /* --- メイン宇宙背景と全体のデザイン調整 --- */
    .stApp {{
        background: radial-gradient(ellipse at bottom, #070b19 0%, #020205 100%) !important;
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        overflow-x: hidden;
    }}

    /* 星空背景 */
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1.5px, transparent 40px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px);
        background-size: 450px 450px, 250px 250px; background-position: 0 0, 40px 60px;
        opacity: 0.25; z-index: 0; pointer-events: none;
    }}

    /* 流れ星 */
    @keyframes shooting-star {{
        0% {{ transform: translateX(0) translateY(0) rotate(-45deg) scale(0); opacity: 0; }}
        5% {{ opacity: 1; transform: translateX(-100px) translateY(100px) rotate(-45deg) scale(1); }}
        15% {{ transform: translateX(-400px) translateY(400px) rotate(-45deg) scale(0); opacity: 0; }}
        100% {{ transform: translateX(-400px) translateY(400px) rotate(-45deg) scale(0); opacity: 0; }}
    }}
    .stApp::after {{
        content: ""; position: fixed; top: 15%; right: -10%; width: 140px; height: 2px;
        background: linear-gradient(-45deg, #00ffff, rgba(0, 0, 0, 0));
        filter: drop-shadow(0 0 6px #00ffff); opacity: 0;
        animation: shooting-star 12s linear infinite; z-index: 0; pointer-events: none;
    }}

    /* タイトルエリア（絶対1列死守・レスポンシブ対応） */
    .cyber-title-container {{
        text-align: center; padding: 15px 10px; margin-bottom: 25px;
        background: rgba(3, 4, 12, 0.85); border: 2px solid #00ffff; border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3), inset 0 0 15px rgba(0, 255, 255, 0.2);
    }}
    .cyber-title {{
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: calc(14px + 2.2vw) !important; color: #ffffff !important;
        text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff; letter-spacing: 1px; margin: 0 !important; white-space: nowrap;
    }}
    .cyber-subtitle {{
        font-size: calc(9px + 0.5vw); color: #ff00ff; text-shadow: 0 0 4px #ff00ff; letter-spacing: 2px; margin-top: 8px; white-space: nowrap;
    }}
    .cyber-credit {{
        font-size: calc(8px + 0.3vw); color: #00ffaa; text-shadow: 0 0 3px #00ffaa; letter-spacing: 1px; margin-top: 10px; white-space: nowrap;
    }}

    h3 {{
        color: #ff55ff !important; text-shadow: 0 0 8px #ff55ff; border-left: 4px solid #ff55ff;
        padding-left: 10px; font-size: calc(16px + 1vw) !important; white-space: nowrap;
    }}
    
    div[data-testid="stMetricLabel"] {{ color: #ffffff !important; font-weight: bold !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important; }}
    div[data-testid="stMetricValue"] {{ color: #00ffaa !important; font-size: 2.3rem !important; text-shadow: 0 0 10px rgba(0, 255, 170, 0.6); }}

    /* --- ラジオボタンと文字の視認性改善 --- */
    .stWidgetLabel, div[data-testid="stMarkdownContainer"] p, label, .stRadio p {{
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 1), 0 0 2px rgba(0, 0, 0, 1) !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }}

    /* ウィジェット背景 */
    div[data-testid="stVerticalBlock"] {{
        background: rgba(5, 8, 22, 0.8) !important; border-radius: 10px; padding: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .stAlert div {{ color: #ffffff !important; }}
</style>
"""

# --- 最初の一度だけオープニング（スプラッシュ）を挟むロジック ---
if "overlay_done" not in st.session_state:
    st.markdown(f"""
    <div class="splash-container">
        <div class="splash-overlay"></div>
        <div class="splash-text">信頼に感謝</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2.2)
    st.session_state.overlay_done = True
    st.rerun()

# --- メイン画面レンダリング（タイトルコンテナを確実にここで射出） ---
st.markdown(space_effects_html, unsafe_allow_html=True)

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

user_role = st.radio("アクセス権限を選択してください：", ["小野田 だいち (借主)", "川端 しづ (貸主)"], horizontal=True)

if user_role == "小野田 だいち (借主)":
    st.info("💡 今月分の50,000円（＋利息）を振り込んだら、下のボタンを押してシグナルを送ってください。")
    if st.button("🚀 返済を実行した（シグナル送信）", disabled=db["daichi_paid"]):
        db["daichi_paid"] = True
        save_data(db)
        st.success("だいちさんの返済シグナルをロックしました。しづさんの承認を待ちます。")
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
st.subheader("📜 分割返済の履歴データ")
if db["history"]:
    for record in reversed(db["history"]):
        st.code(record, language="markdown")
else:
    st.caption("通信記録なし（承認された返済履歴はまだありません）")
