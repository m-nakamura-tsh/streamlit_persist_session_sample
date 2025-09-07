import streamlit as st
from shared import get_storage, save_process_data, render_process_selector

st.set_page_config(
    page_title="詳細表示",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persist process data if available
save_process_data()

# Render process selector in sidebar
available_processes = render_process_selector()

# Get storage instance
storage = get_storage()

st.title("📊 セッション状態詳細")
st.markdown("---")

if not st.session_state.get('selected_process'):
    st.warning("プロセスを選択してください。")
else:
    st.subheader(f"プロセス: {st.session_state.selected_process}")
    
    # Show process info
    process_info = storage.get_process_info(st.session_state.selected_process)
    if process_info:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("作成日時", process_info.get('created', 'N/A'))
        with col2:
            st.metric("最終更新", process_info.get('last_updated', 'N/A'))
    
    st.markdown("---")
    
    # Show current session state (only persist_ keys)
    st.subheader("現在のセッション状態")
    display_data = {}
    for key, value in st.session_state.items():
        if key.startswith('persist_'):
            display_data[key] = value
    
    if display_data:
        st.json(display_data)
    else:
        st.info("セッション状態にデータがありません。")
    
    # Show stored data
    st.subheader("保存済みデータ")
    stored_data = storage.load_process(st.session_state.selected_process)
    if stored_data:
        st.json(stored_data)
    else:
        st.info("保存済みデータがありません。")
    
    # Comparison
    if display_data and stored_data:
        st.subheader("差分")
        
        # Find differences
        only_in_session = set(display_data.keys()) - set(stored_data.keys())
        only_in_storage = set(stored_data.keys()) - set(display_data.keys())
        different_values = []
        
        for key in set(display_data.keys()) & set(stored_data.keys()):
            if display_data[key] != stored_data[key]:
                different_values.append(key)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**セッションのみ:**")
            if only_in_session:
                for key in only_in_session:
                    st.write(f"- {key}")
            else:
                st.write("なし")
        
        with col2:
            st.write("**ストレージのみ:**")
            if only_in_storage:
                for key in only_in_storage:
                    st.write(f"- {key}")
            else:
                st.write("なし")
        
        with col3:
            st.write("**値が異なる:**")
            if different_values:
                for key in different_values:
                    st.write(f"- {key}")
            else:
                st.write("なし")