import streamlit as st
from pathlib import Path
from datetime import datetime
import uuid

# Add packages to path for workspace setup
root_dir = Path(__file__).parent.parent.parent

from persistence import SimpleStorage

# Initialize storage
DATA_PATH = root_dir / "data" / "processes"
storage = SimpleStorage(DATA_PATH)

st.set_page_config(page_title="シンプルプロセステスト", page_icon="🧪")

st.title("🧪 シンプルプロセステスト")
st.markdown("柔軟なデータ永続化機能の動作確認用サンプルアプリ")

st.markdown("---")

# Quick test section
st.header("クイックテスト")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 テストプロセスを作成", use_container_width=True):
        # Create a test process with flexible data structure
        process_name = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}"
        
        # Flexible test data - any JSON serializable structure
        test_data = {
            "persist_担当者": "テストユーザー",
            "persist_ステータス": "実行中",
            "persist_進捗率": 30,
            "persist_優先度": "高",
            "persist_説明": "これはテスト用のプロセスです",
            "persist_タスクリスト": [
                {"名前": "データ取得", "完了": True},
                {"名前": "データ処理", "完了": False},
                {"名前": "レポート生成", "完了": False}
            ],
            "persist_メタデータ": {
                "created_by": "simple_app",
                "test_mode": True,
                "week_number": datetime.now().isocalendar()[1],
                "year": datetime.now().year
            }
        }
        
        storage.save_process(process_name, test_data)
        st.success(f"テストプロセス '{process_name}' を作成しました！")
        st.rerun()

with col2:
    if st.button("🔄 プロセス一覧を更新", use_container_width=True):
        st.rerun()

# List all processes
st.markdown("---")
st.header("すべてのプロセス")

all_processes = storage.list_processes()
if all_processes:
    for process_name in all_processes:
        process_data = storage.load_process(process_name)
        if process_data:
            with st.expander(f"**{process_name}**"):
                # Display flexible process data
                st.subheader("プロセスデータ")
                st.json(process_data)
                
                # Show process metadata
                process_info = storage.get_process_info(process_name)
                if process_info:
                    st.subheader("メタデータ")
                    st.json({
                        "作成日時": process_info.get("created"),
                        "最終更新": process_info.get("last_updated"),
                    })
                
                # Delete button
                if st.button(f"削除", key=f"del_{process_name}"):
                    storage.delete_process(process_name)
                    st.rerun()
else:
    st.info("プロセスがありません。上のボタンでテストプロセスを作成してください。")

# Interactive data editor
st.markdown("---")
st.header("データ編集テスト")

if all_processes:
    selected_process = st.selectbox("編集するプロセスを選択", all_processes)
    
    if selected_process:
        process_data = storage.load_process(selected_process)
        
        if process_data:
            st.subheader("現在のデータ")
            st.json(process_data)
            
            # Simple data editor
            st.subheader("データ編集")
            with st.form("edit_form"):
                new_status = st.selectbox(
                    "ステータス", 
                    ["準備中", "実行中", "完了", "保留"],
                    index=0 if "persist_ステータス" not in process_data else ["準備中", "実行中", "完了", "保留"].index(process_data.get("persist_ステータス", "準備中"))
                )
                new_progress = st.slider(
                    "進捗率", 
                    0, 100, 
                    value=int(process_data.get("persist_進捗率", 0))
                )
                new_description = st.text_area(
                    "説明", 
                    value=process_data.get("persist_説明", "")
                )
                
                if st.form_submit_button("データを更新"):
                    # Update the process data
                    updated_data = process_data.copy()
                    updated_data["persist_ステータス"] = new_status
                    updated_data["persist_進捗率"] = new_progress
                    updated_data["persist_説明"] = new_description
                    
                    storage.save_process(selected_process, updated_data)
                    st.success("データを更新しました！")
                    st.rerun()

# Storage info
with st.sidebar:
    st.header("ストレージ情報")
    st.info(f"保存先: {DATA_PATH}")
    st.metric("総プロセス数", len(all_processes))
    
    st.subheader("特徴")
    st.write("""
    - ✅ 柔軟なデータ構造
    - ✅ JSON serializable なデータ
    - ✅ 自動バリデーション
    - ✅ メタデータ管理
    - ✅ 型安全性
    """)