"""Streamlit session state integration helpers for process management."""
from pathlib import Path
from typing import Any, Dict, Optional, Mapping
from .simple_storage import SimpleStorage


class StreamlitSessionManager:
    """Manages process session data persistence with Streamlit integration."""
    
    def __init__(self, data_path: Path):
        """Initialize the session manager with a data path.
        
        Args:
            data_path: Path to the directory for storing process data
        """
        self.storage = SimpleStorage(data_path)
    
    def load_process_data(self, process_name: str) -> Dict[str, Any]:
        """Load process data from storage.
        
        Args:
            process_name: Name of the process to load
            
        Returns:
            Dictionary containing the process data, or empty dict if not found
        """
        data = self.storage.load_process(process_name)
        if data:
            print(f"loading {process_name} process data... : {data}")
            return data
        return {}
    
    def save_process_data(
        self, 
        process_name: str, 
        session_data: Mapping[str, Any],
        persist_prefix: str = "persist_"
    ) -> None:
        """Save session data to storage, filtering by persist prefix.
        
        Args:
            process_name: Name of the process to save
            session_data: Dictionary containing all session data
            persist_prefix: Prefix to filter keys for persistence (default: "persist_")
        """
        print(f"saving {process_name} process data...")
        self.storage.save_process_with_prefix_filter(process_name, session_data, persist_prefix)
    
    def get_storage(self) -> SimpleStorage:
        """Get the underlying storage instance.
        
        Returns:
            The SimpleStorage instance
        """
        return self.storage
    
    def list_processes(self) -> list[str]:
        """List all available processes.
        
        Returns:
            List of process names
        """
        process_list = self.storage.list_processes()
        # 逆順にソートして表示
        return sorted(process_list, reverse=True)
    
    def process_exists(self, process_name: str) -> bool:
        """Check if a process exists.
        
        Args:
            process_name: Name of the process to check
            
        Returns:
            True if the process exists, False otherwise
        """
        return self.storage.process_exists(process_name)
    
    def get_process_info(self, process_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata about a process.
        
        Args:
            process_name: Name of the process
            
        Returns:
            Dictionary with process metadata or None if not found
        """
        return self.storage.get_process_info(process_name)
    
    def delete_process(self, process_name: str) -> bool:
        """Delete a process.
        
        Args:
            process_name: Name of the process to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        return self.storage.delete_process(process_name)


def load_process_into_session_state(storage: SimpleStorage, process_name: str, session_state: dict) -> None:
    """Load process data into Streamlit session state.
    
    Args:
        storage: Storage instance
        process_name: Name of the process to load
        session_state: Streamlit session state object
    """
    process_data = storage.load_process(process_name)
    if process_data:
        for key, value in process_data.items():
            session_state[key] = value
            print(f"\ton session_state, set {key}:{value}")


def save_session_state_to_process(
    storage: SimpleStorage, 
    process_name: str, 
    session_state: dict,
    persist_prefix: str = "persist_"
) -> None:
    """Save Streamlit session state to process storage with prefix filtering.
    
    Args:
        storage: Storage instance
        process_name: Name of the process to save to
        session_state: Streamlit session state object
        persist_prefix: Prefix to filter keys for persistence
    """
    # Convert session state to regular dict for type compatibility
    session_data = {str(k): v for k, v in session_state.items()}
    storage.save_process_with_prefix_filter(process_name, session_data, persist_prefix)
