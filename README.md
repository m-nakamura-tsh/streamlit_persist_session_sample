# Streamlit Persist Session Sample

Streamlitアプリケーションにおける柔軟なセッション状態の永続化システムのサンプル実装です。

## 概要

このプロジェクトは、Streamlitのセッション状態を長期間（最長1週間）にわたって永続化し、複数のプロセスを並行管理できることを実証するサンプルアプリケーションです。

### 主な特徴

- ✅ **柔軟なデータ構造**: `dict[str, Any]`ベースの自由なデータ管理
- ✅ **自動永続化**: `persist_`プレフィックス付きキーの自動保存
- ✅ **複数プロセス管理**: 名前ベースのプロセス識別と切り替え
- ✅ **Protocol ベース設計**: ダックタイピングによる柔軟な実装
- ✅ **モノレポ構成**: 再利用可能なモジュール管理

## アーキテクチャ

### データ永続化の仕組み

```python
# セッション状態のキーに "persist_" プレフィックスを付けるだけで自動永続化
st.text_input("担当者名", key="persist_担当者名")  # 自動的に永続化される
st.text_input("メモ", key="temp_memo")  # 永続化されない
```

### 柔軟なデータ構造

従来の固定的なモデルクラスから、完全に柔軟な辞書ベースの構造に移行：

```python
# 従来: 固定的なモデル
class ProcessState:
    process_id: str
    status: ProcessStatus
    steps: List[ProcessStep]
    # ... 事前定義が必要

# 現在: 柔軟な辞書構造
process_data = {
    "persist_任意のキー": "任意の値",
    "persist_ネスト構造": {
        "深い": {
            "階層": "も可能"
        }
    },
    "persist_リスト": [1, 2, 3],
    # ... 自由に追加可能
}
```

## プロジェクト構成

```
streamlit_persist_session_sample/
├── packages/
│   └── persistence/          # 永続化レイヤー（Protocol ベース）
│       └── src/
│           ├── simple_storage.py   # シンプルなKey-Value ストレージ
│           ├── interface.py        # Protocol インターフェース
│           └── models.py           # 型定義のみ
├── apps/
│   ├── main/                 # メインアプリケーション
│   └── sample/               # サンプルアプリ
├── data/                     # データ保存ディレクトリ
└── scripts/                  # ユーティリティスクリプト
```

## セットアップ

### 前提条件

- Python 3.9+
- uv (Pythonパッケージマネージャー)

### インストール

1. uvをインストール
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 依存関係をインストール
```bash
uv sync --all-packages
```

## 実行方法

### メインアプリケーションの起動

```bash
./run_main.sh
# または
make run-main
```

### サンプルアプリの起動

```bash
./run_sample.sh
# または
make run-sample
```

## 使い方

### 1. プロセスの作成

「新規プロセス」ページでプロセス名を入力するだけで作成できます。

### 2. セッション状態の永続化

`persist_` プレフィックスを持つキーは自動的に永続化されます：

```python
# 自動的に永続化される
st.text_input("担当者", key="persist_担当者名")
st.slider("進捗", 0, 100, key="persist_進捗率")

# 永続化されない（一時的なUI状態など）
st.checkbox("詳細表示", key="show_details")
```

### 3. プロセスの切り替え

サイドバーでプロセスを選択すると、保存されていたセッション状態が自動的にロードされます。

## 開発

### テストの実行

```bash
uv run pytest packages/persistence/tests/ -v
```

### コードフォーマット

```bash
make format
# または
uv run ruff format .
```

### 型チェック

```bash
make lint
# または
uv run mypy packages/persistence/src/
```

## Protocol ベースの設計

このプロジェクトは Python の Protocol (PEP 544) を使用して、継承なしでインターフェースを定義しています：

```python
from typing import Protocol

class StorageInterface(Protocol):
    def save_process(self, process_name: str, session_data: dict) -> None: ...
    def load_process(self, process_name: str) -> dict | None: ...

# 継承なしで実装
class SimpleStorage:  # StorageInterface を継承しない
    def save_process(self, process_name: str, session_data: dict) -> None:
        # 実装
    def load_process(self, process_name: str) -> dict | None:
        # 実装

# 型チェッカーが自動的に適合性を検証
storage: StorageInterface = SimpleStorage(path)  # OK!
```

## データ管理のベストプラクティス

1. **命名規則**: 永続化したいデータには `persist_` プレフィックスを使用
2. **データ型**: JSON serializable な型のみ使用（文字列、数値、bool、リスト、辞書）
3. **プロセス名**: わかりやすく一意な名前を使用（例: "2025年1月_週次レポート"）

## ライセンス

MIT