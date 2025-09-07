from typing import Protocol, List, Optional
from .models import ProcessData


class StorageInterface(Protocol):
    """Storage interface using Protocol for duck typing with flexible data."""
    
    def save_process(self, process_name: str, session_data: ProcessData) -> None:
        """Save process session data."""
        ...
    
    def load_process(self, process_name: str) -> Optional[ProcessData]:
        """Load process session data by name."""
        ...
    
    def list_processes(self) -> List[str]:
        """List all process names."""
        ...
    
    def delete_process(self, process_name: str) -> bool:
        """Delete a process by name."""
        ...
    
    def process_exists(self, process_name: str) -> bool:
        """Check if process exists."""
        ...