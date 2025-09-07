import streamlit as st

st.set_page_config(
    page_title="シンプルプロセス管理",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 シンプルプロセス管理")
st.markdown("---")

st.write("### ようこそ！")
st.write("このアプリケーションは、長期実行プロセスの状態を柔軟に管理するためのツールです。")

st.markdown("""
### 機能
- **🏠 ワークスペース**: 選択したプロセスの詳細を編集
- **📋 プロセス一覧**: 全プロセスの一覧表示と管理
- **➕ 新規プロセス**: 新しいプロセスの作成
- **📊 詳細表示**: セッション状態と保存データの詳細確認
""")

st.info("左側のサイドバーからページを選択してください。")

# Quick actions
st.subheader("クイックアクション")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 ワークスペースへ", use_container_width=True):
        st.switch_page("pages/1_🏠_ワークスペース.py")

with col2:
    if st.button("📋 プロセス一覧へ", use_container_width=True):
        st.switch_page("pages/2_📋_プロセス一覧.py")

with col3:
    if st.button("➕ 新規プロセス作成", use_container_width=True):
        st.switch_page("pages/3_➕_新規プロセス.py")