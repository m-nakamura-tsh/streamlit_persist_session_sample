"""
Example demonstrating Protocol-based duck typing for storage implementations.

With Protocol, any class that implements the required methods can be used
as a StorageInterface without explicit inheritance.
"""

from typing import TYPE_CHECKING
from pathlib import Path
from datetime import datetime

# Type checking import
if TYPE_CHECKING:
    from .interface import StorageInterface

from .json_storage import JsonStorage
from .models import ProcessState, ProcessStatus


def process_manager(storage: "StorageInterface") -> None:
    """
    This function accepts any object that conforms to StorageInterface protocol.
    No explicit inheritance required - just implement the required methods.
    """
    # List all processes
    processes = storage.list_processes()
    print(f"Found {len(processes)} processes")
    
    # Get running processes
    running = storage.list_processes_by_status(ProcessStatus.RUNNING.value)
    print(f"Running processes: {len(running)}")
    
    # Load and display each process
    for process_id in processes:
        process = storage.load_process(process_id)
        if process:
            print(f"- {process.process_id}: {process.status.value}")


# Example custom storage implementation without explicit inheritance
class CustomMemoryStorage:
    """
    Custom storage that keeps processes in memory.
    This class doesn't inherit from StorageInterface but implements all required methods.
    """
    
    def __init__(self):
        self.processes = {}
    
    def save_process(self, process: ProcessState) -> None:
        self.processes[process.process_id] = process
    
    def load_process(self, process_id: str) -> ProcessState | None:
        return self.processes.get(process_id)
    
    def list_processes(self) -> list[str]:
        return list(self.processes.keys())
    
    def delete_process(self, process_id: str) -> bool:
        if process_id in self.processes:
            del self.processes[process_id]
            return True
        return False
    
    def list_processes_by_status(self, status: str) -> list[str]:
        return [
            pid for pid, process in self.processes.items()
            if process.status.value == status
        ]


def main():
    """Demonstrate duck typing with different storage implementations."""
    
    # Using JsonStorage (no explicit inheritance from StorageInterface)
    json_storage = JsonStorage(Path("/tmp/test_processes"))
    
    # Create a test process
    test_process = ProcessState(
        process_id="test_001",
        week_number=1,
        year=2025,
        status=ProcessStatus.RUNNING,
        started_at=datetime.now()
    )
    
    # Save with JsonStorage
    json_storage.save_process(test_process)
    process_manager(json_storage)  # Works! JsonStorage conforms to protocol
    
    print("\n" + "="*50 + "\n")
    
    # Using CustomMemoryStorage (completely independent implementation)
    memory_storage = CustomMemoryStorage()
    memory_storage.save_process(test_process)
    process_manager(memory_storage)  # Also works! Conforms to protocol
    
    # Type checking will verify both implementations conform to StorageInterface
    # without requiring explicit inheritance


if __name__ == "__main__":
    main()