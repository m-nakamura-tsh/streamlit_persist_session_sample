import streamlit as st
from shared import get_storage, save_process_data, render_process_selector

st.set_page_config(
    page_title="プロセス一覧",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persist process data if available
save_process_data()

# Render process selector in sidebar
available_processes = render_process_selector()

# Get storage instance
storage = get_storage()

st.title("📋 プロセス一覧")
st.markdown("---")

if available_processes:
    for process_name in available_processes:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            process_info = storage.get_process_info(process_name)
            if process_info:
                st.write(f"**{process_name}**")
                st.caption(f"作成: {process_info.get('created', 'N/A')}")
                st.caption(f"最終更新: {process_info.get('last_updated', 'N/A')}")
            else:
                st.write(f"**{process_name}**")
        
        with col2:
            # Don't allow deleting currently selected process
            can_delete = process_name != st.session_state.get('selected_process')
            
            if st.button(
                "削除", 
                key=f"delete_{process_name}",
                disabled=not can_delete,
                help="選択中のプロセスは削除できません" if not can_delete else None
            ):
                if storage.delete_process(process_name):
                    st.success(f"プロセス '{process_name}' を削除しました")
                    st.rerun()
        
        st.divider()
else:
    st.info("プロセスがありません。")
    if st.button("新規プロセスを作成"):
        st.switch_page("pages/3_➕_新規プロセス.py")