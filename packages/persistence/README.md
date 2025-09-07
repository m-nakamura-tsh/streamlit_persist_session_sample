# Persistence Package

Protocol-based永続化レイヤーの実装です。

## 特徴

- **Protocol (PEP 544)** を使用したダックタイピング
- 明示的な継承不要
- 型チェッカー対応（mypy等）
- 実装の切り替えが容易

## Protocol vs ABC

### 従来のABC (Abstract Base Class) 方式
```python
from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def save_process(self, process): pass

class JsonStorage(StorageInterface):  # 明示的な継承が必要
    def save_process(self, process): ...
```

### Protocol方式（現在の実装）
```python
from typing import Protocol

class StorageInterface(Protocol):
    def save_process(self, process): ...

class JsonStorage:  # 継承不要！
    def save_process(self, process): ...
```

## 利点

1. **柔軟性**: 既存のクラスも、必要なメソッドを持っていればStorageInterfaceとして扱える
2. **疎結合**: 実装クラスがインターフェースを知る必要がない
3. **テスタビリティ**: モックオブジェクトの作成が簡単
4. **段階的型付け**: 既存コードへの適用が容易

## 使用例

```python
from persistence import StorageInterface, JsonStorage

def use_storage(storage: StorageInterface):
    """任意のStorageInterface準拠オブジェクトを受け入れる"""
    processes = storage.list_processes()
    # ...

# JsonStorageは明示的にStorageInterfaceを継承していないが使用可能
storage = JsonStorage(Path("./data"))
use_storage(storage)  # OK!

# 独自実装も、必要なメソッドがあれば使用可能
class MyCustomStorage:
    def save_process(self, process): ...
    def load_process(self, process_id): ...
    def list_processes(self): ...
    def delete_process(self, process_id): ...
    def list_processes_by_status(self, status): ...

custom = MyCustomStorage()
use_storage(custom)  # これもOK!
```

## 型チェック

mypyを使用して型の整合性を確認：

```bash
mypy packages/persistence/src/
```

Protocolにより、実装が必要なメソッドを満たしているかを静的にチェックできます。