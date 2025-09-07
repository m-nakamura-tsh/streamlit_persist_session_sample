import streamlit as st
from pathlib import Path
from typing import cast, Dict, Any
from persistence import StreamlitSessionManager

# Initialize session manager
root_dir = Path(__file__).parent.parent.parent
DATA_PATH = root_dir / "data" / "processes"
manager = StreamlitSessionManager(DATA_PATH)

def get_storage():
    """Get storage instance for backward compatibility."""
    return manager.get_storage()

def load_process_data():
    """Load selected process data into session state."""
    if selected_process := st.session_state.get('selected_process'):
        process_data = manager.load_process_data(selected_process)
        if process_data:
            # Overwrite loaded data into session state
            for key, value in process_data.items():
                st.session_state[key] = value
                print(f"\ton session_state, set {key}:{value}")

def save_process_data(process_name: str | None = None):
    """Save current session state to selected process."""
    if st.session_state.get('session_already_saved'):
        # 値を上書きしてしまうので何もしない
        print("pass saving process data")
        # プロセスデータの保存をパスするマークをリセット
        del st.session_state['session_already_saved'] 
        return
    selected_process = process_name or st.session_state.get('selected_process')
    # process name が指定された場合は、session_state側を無視してそちらを利用する 
    if selected_process:
        # Convert SessionStateProxy to Dict[str, Any] to satisfy type checker
        session_data = {str(k): v for k, v in st.session_state.items()}
        manager.save_process_data(selected_process, session_data)

def save_prev_selected_session():
    """一つ前に選択されていたプロセス名し、セッションを保存。デフォルトのセッション保存をパスするようにsession_sateにマークをを指定。"""
    prev_process_name = st.session_state.get('selected_process_prev', None)
    if not prev_process_name:
        pass
    else:
        # 過去のプロセス名でセッションを保存
        save_process_data(process_name=prev_process_name)
    new_process_name = st.session_state['selected_process']
    # デフォルトで呼ばれるセッション保存をパスするようにマーク
    st.session_state['session_already_saved'] = True
    # 過去のプロセス名を更新
    st.session_state["selected_process_prev"] = new_process_name

def render_process_selector():
    """Render process selector in sidebar."""
    available_processes = manager.list_processes()
    
    st.sidebar.header("プロセス選択")
    
    if available_processes:
        selected = st.sidebar.selectbox(
            "現在のプロセス",
            available_processes,
            key='selected_process',
            on_change=save_prev_selected_session,
        )
        
        if selected:
            print(f"process is selected. {selected}")
            load_process_data()
            process_info = manager.get_process_info(selected)
            if process_info:
                st.sidebar.info(f"最終更新: {process_info.get('last_updated', 'N/A')}")
        
        st.sidebar.divider()
    else:
        st.sidebar.warning("プロセスがありません。新規作成してください。")
    
    return available_processes
