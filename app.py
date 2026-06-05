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
