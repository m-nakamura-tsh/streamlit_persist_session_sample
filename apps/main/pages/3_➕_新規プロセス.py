import streamlit as st
from pathlib import Path

from persistence import SimpleStorage

# Add packages to path for workspace setup
root_dir = Path(__file__).parent.parent.parent.parent

# Initialize storage
DATA_PATH = root_dir / "data" / "processes"
storage = SimpleStorage(DATA_PATH)

st.set_page_config(page_title="新規プロセス", page_icon="➕", layout="wide")

st.title("➕ 新規プロセス作成")

st.write("シンプルな新規プロセスを作成します。プロセス名を指定するだけで作成できます。")

# Process creation form
with st.form("new_process_form"):
    st.subheader("プロセス情報")
    
    process_name = st.text_input(
        "プロセス名",
        placeholder="例: 2025年1月週次レポート",
        help="プロセスを識別するための名前を入力してください"
    )
    
    # Optional initial values
    st.subheader("初期値（オプション）")
    initial_担当者名 = st.text_input("初期担当者名", placeholder="田中太郎")
    initial_説明 = st.text_area("初期説明", placeholder="このプロセスの概要を記述...")
    initial_ステータス = st.selectbox("初期ステータス", ["準備中", "実行中", "完了", "保留"])
    
    submitted = st.form_submit_button("プロセスを作成", type="primary", use_container_width=True)

if submitted:
    if not process_name.strip():
        st.error("プロセス名を入力してください。")
    elif storage.process_exists(process_name):
        st.error(f"プロセス名 '{process_name}' は既に存在します。別の名前を使用してください。")
    else:
        # Create initial session data with persist_ prefix
        initial_data = {}
        
        if initial_担当者名:
            initial_data['persist_担当者名'] = initial_担当者名
        if initial_説明:
            initial_data['persist_説明'] = initial_説明
        if initial_ステータス:
            initial_data['persist_ステータス'] = initial_ステータス
        
        # Default values
        if 'persist_進捗率' not in initial_data:
            initial_data['persist_進捗率'] = 0
        if 'persist_優先度' not in initial_data:
            initial_data['persist_優先度'] = "中"
        
        # Save new process
        storage.save_process(process_name, initial_data)
        
        st.success(f"✅ プロセス '{process_name}' を作成しました！")
        
        # Navigation options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("メインページへ", use_container_width=True):
                # Set the newly created process as selected
                st.session_state['selected_process'] = process_name
                st.switch_page("app.py")
        with col2:
            if st.button("別のプロセスを作成", use_container_width=True):
                st.rerun()

# Show existing processes for reference
st.markdown("---")
st.subheader("既存プロセス一覧")

existing_processes = storage.list_processes()
if existing_processes:
    st.write("参考: 既に作成されているプロセス")
    for process_name in existing_processes:
        process_info = storage.get_process_info(process_name)
        if process_info:
            st.write(f"- **{process_name}** (作成: {process_info.get('created', 'N/A')})")
        else:
            st.write(f"- **{process_name}**")
else:
    st.info("まだプロセスが作成されていません。")