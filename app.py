import streamlit as st
import datetime
import json
import os

# ==========================================
# 1. 宇宙ベース（近未来的）UIのカスタムCSS
# ==========================================
st.set_page_config(page_title="SpaceLab Repayment Core", page_icon="🚀", layout="centered")

space_css = """
<style>
    /* 全体の背景とテキストカラー（ディープスペース） */
    .stApp {
        background-color: #03030d;
        color: #e0e0ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* タイトルとヘッダーのネオンエフェクト */
    h1 {
        color: #00ffff !important;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        text-align: center;
        letter-spacing: 2px;
    }
    h3 {
        color: #ff00ff !important;
        text-shadow: 0 0 5px #ff00ff;
    }
    
    /* サイバーパンク風メトリクス（残高表示など） */
    div[data-testid="stMetricValue"] {
        color: #00ffaa !important;
        font-size: 2.5rem !important;
        text-shadow: 0 0 8px #00ffaa;
    }
    
    /* ステータスボックスの宇宙的カスタマイズ */
    .stAlert {
        background-color: #0a0a23 !important;
        border: 1px solid #00ffff !important;
        color: #00ffff !important;
    }
</style>
"""
st.markdown(space_css, unsafe_allow_html=True)

# ==========================================
# 2. データ管理ロジック（簡易ファイルモック）
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

# データの初期化
if 'db' not in st.session_state:
    st.session_state.db = load_data()

db = st.session_state.db

# ==========================================
# 3. メインUIコンテンツ
# ==========================================
st.title("🌌 REPAYMENT MANAGEMENT SYSTEM")
st.write("---")

# 残高・ステータス表示（コックピット風）
col1, col2 = st.columns(2)
with col1:
    st.metric(label="☄️ INITIAL LOAN", value="¥701,000")
with col2:
    st.metric(label="🛰️ CURRENT REMAINING", value=f"¥{db['remaining_amount']:,}")

st.write("---")

# 現在の返済サイクル（今月の状況）
st.subheader("🛸 Current Cycle Status")

# 相互ロック判定のインジケーター
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

# ユーザー切り替え（iPhone等からのアクセスを想定し簡易エミュレート）
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
        
        # 両者のボタンが押されたので、ここで初めて残高を減らす（5万円マイナス）
        # ※投資収益等での増額返済に対応する場合は、金額を入力可能にするアレンジも可能です。
        repay_unit = 50000 
        db["remaining_amount"] = max(0, db["remaining_amount"] - repay_unit)
        
        # 履歴への追加
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        db["history"].append(f"{now_str} : ¥{repay_unit:,} の返済が承認されました。")
        
        # 次回サイクルのためにフラグをリセット
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
