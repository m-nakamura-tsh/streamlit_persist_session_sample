import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import ProcessState, AuditEntry


class JsonStorage:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, process_id: str) -> Path:
        return self.base_path / f"{process_id}.json"
    
    def save_process(self, process: ProcessState) -> None:
        file_path = self._get_file_path(process.process_id)
        
        # Add audit entry for save operation
        audit_entry = AuditEntry(
            timestamp=datetime.now(),
            action="save_process",
            details={"status": process.status.value}
        )
        process.audit_trail.append(audit_entry)
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(process.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_process(self, process_id: str) -> Optional[ProcessState]:
        file_path = self._get_file_path(process_id)
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return ProcessState.from_dict(data)
    
    def list_processes(self) -> List[str]:
        process_files = self.base_path.glob("*.json")
        return [f.stem for f in process_files]
    
    def delete_process(self, process_id: str) -> bool:
        file_path = self._get_file_path(process_id)
        
        if file_path.exists():
            # Create backup before deletion (for audit purposes)
            backup_path = self.base_path / "deleted" / f"{process_id}_{datetime.now().isoformat()}.json"
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.rename(backup_path)
            return True
        
        return False
    
    def list_processes_by_status(self, status: str) -> List[str]:
        matching_processes = []
        
        for process_id in self.list_processes():
            process = self.load_process(process_id)
            if process and process.status.value == status:
                matching_processes.append(process_id)
        
        return matching_processes