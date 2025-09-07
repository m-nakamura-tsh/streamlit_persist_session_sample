import streamlit as st
from shared import save_process_data, render_process_selector

st.set_page_config(
    page_title="ワークスペース",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persist process data if available
save_process_data()

# Render process selector in sidebar
available_processes = render_process_selector()

def render_step_navigation():
    """サイドバーにステップ進捗とナビゲーションを表示"""
    st.sidebar.divider()
    st.sidebar.header("📋 ステップ進捗")
    
    # 現在のステップを取得（デフォルトは1）
    current_step = st.session_state.get('persist_current_step', 1)
    
    # ステップ進捗表示
    steps = [
        {"number": 1, "title": "基本情報", "icon": "📝"},
        {"number": 2, "title": "詳細情報", "icon": "📋"},
        {"number": 3, "title": "チェックリスト", "icon": "✅"}
    ]
    
    for step in steps:
        if step["number"] == current_step:
            st.sidebar.success(f"🔄 **Step.{step['number']}**: {step['title']}")
        elif step["number"] < current_step:
            st.sidebar.success(f"✅ Step.{step['number']}: {step['title']}")
        else:
            st.sidebar.info(f"{step['icon']} Step.{step['number']}: {step['title']}")
    
    st.sidebar.divider()

    # 完了率表示
    completion_rate = (current_step -1) / len(steps)
    st.sidebar.progress(completion_rate)
    st.sidebar.caption(f"完了率: {completion_rate * 100:.0f}% ({current_step -1}/{len(steps)} ステップ完了)")
    
    st.sidebar.divider()
    
    # ナビゲーションボタン
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("⬅️ 前へ", disabled=(current_step <= 1), key="prev_step"):
            st.session_state['persist_current_step'] = max(1, current_step - 1)
            st.rerun()
    
    with col2:
        if st.button("次へ ➡️", disabled=(current_step >= 3), key="next_step"):
            st.session_state['persist_current_step'] = min(3, current_step + 1)
            st.rerun()
    
    return current_step

# ステップナビゲーション表示
current_step = render_step_navigation()

st.title("🏠 ワークスペース")
st.markdown("---")

# Main content - Workspace only
if not st.session_state.get('selected_process'):
    st.warning("プロセスを選択するか、新規作成してください。")
    st.stop()

st.header(f"プロセス: {st.session_state.selected_process}")
st.info(f"現在のステップ: **Step.{current_step}**")

def render_step_1():
    """Step.1: 基本情報"""
    st.subheader("📝 Step.1: 基本情報")
    st.markdown("プロセスの基本的な情報を入力してください。")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("担当者名", key='persist_担当者名')
        status = st.selectbox("ステータス", ["準備中", "実行中", "完了", "保留"], key='persist_ステータス')
    
    with col2:
        progress = st.slider("進捗率", 0, 100, key='persist_進捗率')

def render_step_2():
    """Step.2: 詳細情報"""
    st.subheader("📋 Step.2: 詳細情報")
    st.markdown("プロセスの詳細な説明と優先度を設定してください。")
    st.markdown("---")
    
    description = st.text_area("説明", key='persist_説明', height=150)
    priority = st.radio("優先度", ["低", "中", "高"], key='persist_優先度', horizontal=True)

def render_step_3():
    """Step.3: チェックリスト"""
    st.subheader("✅ Step.3: チェックリスト")
    st.markdown("各タスクの完了状況をチェックしてください。")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        task1 = st.checkbox("タスク1: 初期設定", key='persist_task1')
        task2 = st.checkbox("タスク2: データ収集", key='persist_task2')
    
    with col2:
        task3 = st.checkbox("タスク3: 分析実行", key='persist_task3')
        task4 = st.checkbox("タスク4: レポート作成", key='persist_task4')
    
    # 完了率表示
    completed_tasks = sum([task1, task2, task3, task4])
    completion_rate = (completed_tasks / 4) * 100
    st.progress(completion_rate / 100)
    st.caption(f"完了率: {completion_rate:.0f}% ({completed_tasks}/4 タスク完了)")

# 現在のステップに応じてコンテンツを表示
if current_step == 1:
    render_step_1()
elif current_step == 2:
    render_step_2()
elif current_step == 3:
    render_step_3()

# ステップ操作ボタンをメインエリアにも表示
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if current_step > 1:
        if st.button("⬅️ 前のステップ", key="main_prev"):
            st.session_state['persist_current_step'] = current_step - 1
            st.rerun()

with col3:
    if current_step < 3:
        if st.button("次のステップ ➡️", key="main_next"):
            st.session_state['persist_current_step'] = current_step + 1
            st.rerun()
