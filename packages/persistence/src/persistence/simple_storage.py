import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .models import JsonSerializable, ProcessData


class SimpleStorage:
    """
    Simplified storage for session state persistence.
    Stores process data as simple key-value pairs where:
    - key: process name (string)
    - value: session state data (dict)
    """
    
    def __init__(self, base_path: Path) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.data_file = self.base_path / "processes.json"
        self.data: Dict[str, Dict[str, Any]] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Load all process data from file."""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {}
    
    def _save_data(self) -> None:
        """Save all process data to file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def _validate_data(self, data: ProcessData) -> bool:
        """Validate that all values are JSON serializable."""
        try:
            json.dumps(data)
            return True
        except (TypeError, ValueError):
            return False
    
    def save_process(self, process_name: str, session_data: ProcessData) -> None:
        """Save process session state data."""
        if not self._validate_data(session_data):
            raise ValueError(f"Session data contains non-serializable values for process '{process_name}'")
        
        # Add metadata
        process_data = {
            "session_data": session_data,
            "last_updated": datetime.now().isoformat(),
            "created": self.data.get(process_name, {}).get("created", datetime.now().isoformat())
        }
        
        self.data[process_name] = process_data
        self._save_data()

    def save_process_with_prefix_filter(
        self, 
        process_name: str, 
        session_data: ProcessData, 
        persist_prefix: str = "persist_"
    ) -> None:
        """Save session data to storage, filtering by persist prefix.
        
        Args:
            process_name: Name of the process to save
            session_data: Dictionary containing all session data
            persist_prefix: Prefix to filter keys for persistence (default: "persist_")
        """
        filtered_data = {}
        for key, value in session_data.items():
            if key.startswith(persist_prefix):
                try:
                    json.dumps(value)  # Test if serializable
                    filtered_data[key] = value
                except (TypeError, ValueError):
                    # Skip non-serializable values
                    pass
        
        self.save_process(process_name, filtered_data)
    
    def load_process(self, process_name: str) -> Optional[ProcessData]:
        """Load process session state data."""
        process_data = self.data.get(process_name)
        if process_data:
            return process_data.get("session_data", {})
        return None
    
    def list_processes(self) -> List[str]:
        """List all process names."""
        return list(self.data.keys())
    
    def delete_process(self, process_name: str) -> bool:
        """Delete a process."""
        if process_name in self.data:
            del self.data[process_name]
            self._save_data()
            return True
        return False
    
    def get_process_info(self, process_name: str) -> Optional[Dict[str, Any]]:
        """Get process metadata (creation date, last updated)."""
        return self.data.get(process_name)
    
    def process_exists(self, process_name: str) -> bool:
        """Check if process exists."""
        return process_name in self.data