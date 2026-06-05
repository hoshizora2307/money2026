import streamlit as st
import datetime
import json
import os

# ==========================================
# 1. 宇宙ベース(高視認性サイバー)カスタムCSS/HTML
# ==========================================
st.set_page_config(page_title="返済管理システム Core", page_icon="🚀", layout="centered")

space_effects_html = """
<style>
    /* 全体の背景を深い宇宙に設定 */
    .stApp {
        background: radial-gradient(ellipse at bottom, #070b19 0%, #020205 100%) !important;
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        overflow-x: hidden;
    }

    /* 星空レイヤー（少し暗めにして文字を邪魔しないように調整） */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1.5px, transparent 40px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px);
        background-size: 450px 450px, 250px 250px;
        background-position: 0 0, 40px 60px;
        opacity: 0.25;
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

    /* --- 太陽系惑星オービットシステム --- */
    @keyframes orbit-rotate {
        from { transform: translate(-50%, -50%) rotate(0deg); }
        to { transform: translate(-50%, -50%) rotate(360deg); }
    }
    .solar-system {
        position: fixed;
        top: 50%; left: 50%; width: 0px; height: 0px;
        z-index: 0; pointer-events: none; opacity: 0.15;
    }
    .sun-glow {
        position: absolute;
        width: 100px; height: 100px;
        background: radial-gradient(circle, rgba(255,150,0,0.3) 0%, transparent 70%);
        transform: translate(-50%, -50%);
    }
    .orbit {
        position: absolute;
        border: 1px dashed rgba(0, 255, 255, 0.15);
        border-radius: 50%;
        animation: orbit-rotate linear infinite;
    }
    .planet { position: absolute; top: 0; left: 50%; border-radius: 50%; transform: translate(-50%, -50%); }
    .orbit-inner { width: 280px; height: 280px; animation-duration: 25s; }
    .planet-inner { width: 10px; height: 10px; background: #00bfff; box-shadow: 0 0 8px #00bfff; }
    .orbit-outer { width: 520px; height: 520px; animation-duration: 50s; }
    .planet-outer { width: 16px; height: 16px; background: #ffaa44; box-shadow: 0 0 10px #ffaa44; }

    /* --- 【重要】視認性最優先のUI調整 --- */
    
    /* タイトルコンテナ */
    .cyber-title-container {
        text-align: center;
        padding: 15px 10px;
        margin-bottom: 25px;
        background: rgba(3, 4, 12, 0.85);
        border: 2px solid #00ffff;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3), inset 0 0 15px rgba(0, 255, 255, 0.2);
    }
    .cyber-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: calc(14px + 2.2vw) !important;
        color: #ffffff !important;
        text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
        letter-spacing: 1px;
        margin: 0 !important;
        white-space: nowrap;
    }
    .cyber-subtitle {
        font-size: calc(9px + 0.5vw); color: #ff00ff;
        text-shadow: 0 0 4px #ff00ff; letter-spacing: 2px; margin-top: 8px;
        white-space: nowrap;
    }
    .cyber-credit {
        font-size: calc(8px + 0.3vw); color: #00ffaa;
        text-shadow: 0 0 3px #00ffaa; letter-spacing: 1px; margin-top: 10px;
        white-space: nowrap;
    }

    /* セクションヘッダー(紫ネオン) */
    h3 {
        color: #ff55ff !important;
        text-shadow: 0 0 8px #ff55ff;
        border-left: 4px solid #ff55ff;
        padding-left: 10px;
        font-size: calc(16px + 1vw) !important;
        white-space: nowrap;
    }
    
    /* メトリクス（数値表示）のラベルを明るい白ベースに変更して視認性確保 */
    div[data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important;
        font-size: 1rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #00ffaa !important;
        font-size: 2.3rem !important;
        text-shadow: 0 0 10px rgba(0, 255, 170, 0.6);
    }

    /* ラジオボタン・テキストラベルの文字色を「絶対的な白」に強制 */
    .stWidgetLabel, div[data-testid="stMarkdownContainer"] p, label {
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 1), 0 0 2px rgba(0, 0, 0, 1) !important;
        font-weight: 500 !important;
    }

    /* ウィジェット全体の背景を少し暗くして文字を浮かび上がらせる */
    div[data-testid="stVerticalBlock"] {
        background: rgba(5, 8, 22, 0.75) !important;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* インフォメーションボックスの文字も見やすく調整 */
    .stAlert div {
        color: #ffffff !important;
    }
</style>

<div class="solar-system">
    <div class="sun-glow"></div>
    <div class="orbit orbit-inner"><div class="planet planet-inner"></div></div>
    <div class="orbit orbit-outer"><div class="planet planet-outer"></div></div>
</div>

<div class="cyber-title-container">
    <div class="cyber-title">⚡ 返済管理コアシステム ⚡</div>
    <div class="cyber-subtitle">SYSTEM VER 1.00 / 相互ロック制御</div>
    <div class="cyber-credit">BY HOSHIZORA2307 SOFTWARE SYSTEMS</div>
</div>
"""
st.markdown(space_effects_html, unsafe_allow_html=True)

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
