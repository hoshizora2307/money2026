import streamlit as st
import datetime
import json
import os

# ==========================================
# 1. 満天の流星群 ＆ 完全CSSシバイヌマスコット ＆ メッセージ
# ==========================================
st.set_page_config(page_title="返済管理システム Core", page_icon="🚀", layout="centered")

space_max_meteors_html = """
<style>
    /* --------------------------------------------------
       [超強化] 画面全体の至る所に降り注ぐ流星群システム
    -------------------------------------------------- */
    .stApp {
        background: radial-gradient(ellipse at bottom, #060d1f 0%, #010206 100%) !important;
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        overflow-x: hidden;
    }

    /* 基本の星空 */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 40px),
            radial-gradient(rgba(255,255,255,0.15), rgba(255,255,255,0.08) 1px, transparent 30px);
        background-size: 250px 250px, 150px 150px; 
        opacity: 0.35; z-index: 0; pointer-events: none;
    }

    /* 流れ星のアニメーション共通設計 */
    @keyframes super-meteor {
        0% { transform: translateX(0) translateY(0) rotate(-40deg); opacity: 0; width: 0px; }
        5% { opacity: 1; width: 100px; }
        20% { transform: translateX(-400px) translateY(400px) rotate(-40deg); opacity: 0; width: 0px; }
        100% { transform: translateX(-400px) translateY(400px) rotate(-40deg); opacity: 0; }
    }

    /* 至る所に配置する流れ星コンポーネント群 */
    .meteor {
        position: fixed; width: 2px; height: 2px; opacity: 0; z-index: 1; pointer-events: none;
        animation: super-meteor infinite ease-in-out;
    }
    
    /* 位置・タイミング・速度の分散バラバラ配置 */
    .m1 { top: -20px; right: 10%; background: linear-gradient(-40deg, #ffffff, transparent); filter: drop-shadow(0 0 6px #00ffaa); animation-duration: 5s; animation-delay: 0s; }
    .m2 { top: -20px; right: 35%; background: linear-gradient(-40deg, #ffffff, transparent); filter: drop-shadow(0 0 6px #ff00ff); animation-duration: 7s; animation-delay: 2s; }
    .m3 { top: 10%; right: 5%; background: linear-gradient(-40deg, #ffffff, transparent); filter: drop-shadow(0 0 5px #00ffff); animation-duration: 6s; animation-delay: 4s; }
    .m4 { top: -20px; right: 60%; background: linear-gradient(-40deg, #ffffff, transparent); filter: drop-shadow(0 0 8px #ffffff); animation-duration: 8s; animation-delay: 1s; }
    .m5 { top: 20%; right: 40%; background: linear-gradient(-40deg, #ffffff, transparent); filter: drop-shadow(0 0 6px #00ff41); animation-duration: 4s; animation-delay: 3s; }
    .m6 { top: -20px; right: 80%; background: linear-gradient(-40deg, #ffffff, transparent); filter: drop-shadow(0 0 6px #ffaa00); animation-duration: 9s; animation-delay: 5.5s; }
    .m7 { top: 30%; right: 20%; background: linear-gradient(-40deg, #ffffff, transparent); filter: drop-shadow(0 0 5px #00ffaa); animation-duration: 6.5s; animation-delay: 1.5s; }

    /* --------------------------------------------------
       [100%確実] CSSネイティブ造形・スペースシバイヌ
    -------------------------------------------------- */
    @keyframes shiba-space-float {
        0% { transform: translateY(0px) rotate(-5deg); }
        50% { transform: translateY(-20px) rotate(8deg); }
        100% { transform: translateY(0px) rotate(-5deg); }
    }

    .shiba-space-box {
        position: fixed; bottom: 50px; right: 30px; width: 70px; height: 70px;
        z-index: 9999; pointer-events: none;
        animation: shiba-space-float 4.5s ease-in-out infinite;
    }

    /* 宇宙服のバブルヘルメット */
    .shiba-helmet-bubble {
        width: 100%; height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(0,255,170,0.08) 70%, transparent 100%);
        border: 2px solid rgba(0, 255, 170, 0.5); border-radius: 50%;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.4), inset 0 0 10px rgba(255,255,255,0.3);
        display: flex; align-items: center; justify-content: center; position: relative;
    }

    /* CSSで作る柴犬の顔・体構造 */
    .css-shiba-face {
        position: relative; width: 36px; height: 32px;
        background: #e68a00; /* 柴犬オレンジ */
        border-radius: 20px 20px 16px 16px;
    }
    /* 白いマズル（泥棒ひげエリア） */
    .css-shiba-face::before {
        content: ""; position: absolute; bottom: 0; left: 4px; width: 28px; height: 14px;
        background: #ffffff; border-radius: 0 0 12px 12px; z-index: 1;
    }
    /* つぶらな黒目 */
    .css-shiba-face::after {
        content: "•  •"; position: absolute; top: 8px; left: 8px;
        color: #222222; font-size: 14px; font-weight: bold; word-spacing: 4px; line-height: 1;
    }
    /* 三角の黒鼻 */
    .shiba-nose {
        position: absolute; bottom: 10px; left: 16px; width: 4px; height: 3px;
        background: #222222; border-radius: 50%; z-index: 2;
    }
    /* ピンと立った耳 (左・右) */
    .shiba-ear-l, .shiba-ear-r {
        position: absolute; top: -6px; width: 0; height: 0;
        border-bottom: 10px solid #e68a00; border-left: 6px solid transparent; border-right: 6px solid transparent;
    }
    .shiba-ear-l { left: 2px; transform: rotate(-15deg); }
    .shiba-ear-r { right: 2px; transform: rotate(15deg); }

    /* くるんと丸まった可愛い巻き尾 */
    .shiba-tail {
        position: absolute; bottom: -4px; right: -4px; width: 14px; height: 14px;
        background: #e68a00; border: 2px solid #ffffff; border-radius: 50%;
    }

    /* --------------------------------------------------
       [独立制御] マトリックス風・起動メッセージ演出
    -------------------------------------------------- */
    @keyframes matrix-flash-gate {
        0% { opacity: 1; visibility: visible; }
        85% { opacity: 1; visibility: visible; }
        100% { opacity: 0; visibility: hidden; }
    }
    @keyframes matrix-text-glow {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.9); filter: blur(4px); letter-spacing: 2px; }
        20% { opacity: 1; filter: blur(0px); letter-spacing: 6px; text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ffaa; }
        80% { opacity: 1; transform: translate(-50%, -50%) scale(1.03); letter-spacing: 8px; text-shadow: 0 0 15px #00ff41, 0 0 30px #00ffaa; }
        100% { opacity: 0; filter: blur(2px); transform: translate(-50%, -50%) scale(1.05); }
    }

    .matrix-overlay-gate {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(1, 3, 10, 0.65); backdrop-filter: blur(2px);
        z-index: 999999; pointer-events: none;
        animation: matrix-flash-gate 2.5s steps(25, end) forwards;
    }
    .matrix-neon-text {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        color: #ffffff; font-family: 'Noto Serif JP', 'Georgia', serif;
        font-size: calc(22px + 1.8vw); font-weight: bold; white-space: nowrap;
        animation: matrix-text-glow 2.4s ease-in-out forwards;
    }

    /* --------------------------------------------------
       サイバーUIコンポーネント
    -------------------------------------------------- */
    .cyber-title-container {
        text-align: center; padding: 18px 10px; margin-bottom: 25px;
        background: rgba(4, 10, 26, 0.85); border: 2px solid #00ffaa; border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.2), inset 0 0 15px rgba(0, 255, 170, 0.1);
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
        color: #00ffaa !important; text-shadow: 0 0 8px rgba(0,255,170,0.3); border-left: 4px solid #00ffaa;
        padding-left: 10px; font-size: calc(15px + 0.8vw) !important; white-space: nowrap;
    }
    
    div[data-testid="stMetricLabel"] { color: #ffffff !important; font-weight: bold !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important; }
    div[data-testid="stMetricValue"] { color: #00ffaa !important; font-size: 2.2rem !important; text-shadow: 0 0 10px rgba(0, 255, 170, 0.3); }

    .stWidgetLabel, div[data-testid="stMarkdownContainer"] p, label, .stRadio p {
        color: #ffffff !important; text-shadow: 1px 1px 4px rgba(0, 0, 0, 1) !important; font-weight: 600 !important;
    }

    div[data-testid="stVerticalBlock"] {
        background: rgba(5, 12, 30, 0.75) !important; border-radius: 10px; padding: 14px;
        border: 1px solid rgba(0, 255, 170, 0.2);
    }
    .stAlert div { color: #ffffff !important; }
</style>

<div class="meteor m1"></div>
<div class="meteor m2"></div>
<div class="meteor m3"></div>
<div class="meteor m4"></div>
<div class="meteor m5"></div>
<div class="meteor m6"></div>
<div class="meteor m7"></div>

<div class="shiba-space-box">
    <div class="shiba-helmet-bubble">
        <div class="css-shiba-face">
            <div class="shiba-ear-l"></div>
            <div class="shiba-ear-r"></div>
            <div class="shiba-nose"></div>
            <div class="shiba-tail"></div>
        </div>
    </div>
</div>

<div class="matrix-overlay-gate">
    <div class="matrix-neon-text">信頼に感謝</div>
</div>
"""

st.markdown(space_max_meteors_html, unsafe_allow_html=True)

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
