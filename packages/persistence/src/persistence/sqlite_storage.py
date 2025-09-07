# SQLite implementation placeholder for future use
from typing import List, Optional
from pathlib import Path
from .models import ProcessState


class SqliteStorage:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        # TODO: Implement SQLite storage
        raise NotImplementedError("SQLite storage not yet implemented")
    
    def save_process(self, process: ProcessState) -> None:
        raise NotImplementedError
    
    def load_process(self, process_id: str) -> Optional[ProcessState]:
        raise NotImplementedError
    
    def list_processes(self) -> List[str]:
        raise NotImplementedError
    
    def delete_process(self, process_id: str) -> bool:
        raise NotImplementedError
    
    def list_processes_by_status(self, status: str) -> List[str]:
        raise NotImplementedError