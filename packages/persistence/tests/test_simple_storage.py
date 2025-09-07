import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime

from persistence import SimpleStorage, ProcessData, JsonSerializable


class TestSimpleStorage:
    """Test cases for flexible data storage using SimpleStorage."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage instance for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield SimpleStorage(Path(temp_dir))
    
    def test_basic_data_storage(self, temp_storage):
        """Test basic data storage and retrieval."""
        process_name = "test_process"
        test_data = {
            "persist_string": "hello world",
            "persist_number": 42,
            "persist_float": 3.14,
            "persist_boolean": True,
            "persist_null": None
        }
        
        # Save and load
        temp_storage.save_process(process_name, test_data)
        loaded_data = temp_storage.load_process(process_name)
        
        assert loaded_data == test_data
    
    def test_complex_data_structures(self, temp_storage):
        """Test complex nested data structures."""
        process_name = "complex_test"
        complex_data = {
            "persist_list": [1, 2, 3, "text", True, None],
            "persist_dict": {
                "nested": {
                    "deeply": {
                        "nested": "value"
                    }
                }
            },
            "persist_mixed": [
                {"name": "item1", "value": 100},
                {"name": "item2", "value": 200}
            ]
        }
        
        temp_storage.save_process(process_name, complex_data)
        loaded_data = temp_storage.load_process(process_name)
        
        assert loaded_data == complex_data
    
    def test_data_validation(self, temp_storage):
        """Test data validation for non-serializable data."""
        process_name = "validation_test"
        
        # Valid data should work
        valid_data = {"persist_valid": "test"}
        temp_storage.save_process(process_name, valid_data)
        
        # Invalid data should raise ValueError
        invalid_data = {"persist_invalid": lambda x: x}  # Functions are not JSON serializable
        
        with pytest.raises(ValueError, match="non-serializable values"):
            temp_storage.save_process(process_name, invalid_data)
    
    def test_process_management(self, temp_storage):
        """Test process management operations."""
        # Create multiple processes
        processes = {
            "process_1": {"persist_data": "value1"},
            "process_2": {"persist_data": "value2"},
            "process_3": {"persist_data": "value3"}
        }
        
        for name, data in processes.items():
            temp_storage.save_process(name, data)
        
        # List processes
        process_list = temp_storage.list_processes()
        assert len(process_list) == 3
        assert all(name in process_list for name in processes.keys())
        
        # Delete a process
        assert temp_storage.delete_process("process_2") is True
        assert temp_storage.delete_process("nonexistent") is False
        
        updated_list = temp_storage.list_processes()
        assert len(updated_list) == 2
        assert "process_2" not in updated_list
    
    def test_process_existence(self, temp_storage):
        """Test process existence checking."""
        process_name = "existence_test"
        test_data = {"persist_test": "data"}
        
        # Initially should not exist
        assert temp_storage.process_exists(process_name) is False
        
        # After saving should exist
        temp_storage.save_process(process_name, test_data)
        assert temp_storage.process_exists(process_name) is True
        
        # After deletion should not exist
        temp_storage.delete_process(process_name)
        assert temp_storage.process_exists(process_name) is False
    
    def test_metadata_management(self, temp_storage):
        """Test metadata creation and retrieval."""
        process_name = "metadata_test"
        test_data = {"persist_test": "metadata"}
        
        # Save process
        temp_storage.save_process(process_name, test_data)
        
        # Get metadata
        metadata = temp_storage.get_process_info(process_name)
        assert metadata is not None
        assert "created" in metadata
        assert "last_updated" in metadata
        assert "session_data" in metadata
        
        # Verify timestamps are valid ISO format
        created = datetime.fromisoformat(metadata["created"])
        updated = datetime.fromisoformat(metadata["last_updated"])
        assert isinstance(created, datetime)
        assert isinstance(updated, datetime)
    
    def test_data_persistence(self, temp_storage):
        """Test that data persists across storage instances."""
        process_name = "persistence_test"
        test_data = {"persist_persistent": "this should persist"}
        
        # Save data
        temp_storage.save_process(process_name, test_data)
        
        # Create new storage instance with same path
        new_storage = SimpleStorage(temp_storage.base_path)
        
        # Data should still be there
        loaded_data = new_storage.load_process(process_name)
        assert loaded_data == test_data
    
    def test_empty_data(self, temp_storage):
        """Test handling of empty data."""
        process_name = "empty_test"
        empty_data = {}
        
        temp_storage.save_process(process_name, empty_data)
        loaded_data = temp_storage.load_process(process_name)
        
        assert loaded_data == empty_data
    
    def test_nonexistent_process_load(self, temp_storage):
        """Test loading non-existent process returns None."""
        result = temp_storage.load_process("nonexistent_process")
        assert result is None
    
    def test_json_serializable_types(self, temp_storage):
        """Test various JSON serializable types."""
        process_name = "types_test"
        
        # Test all basic JSON serializable types
        test_data = {
            "persist_str": "string",
            "persist_int": 42,
            "persist_float": 3.14159,
            "persist_bool_true": True,
            "persist_bool_false": False,
            "persist_none": None,
            "persist_empty_list": [],
            "persist_empty_dict": {},
            "persist_list_mixed": ["str", 1, 3.14, True, None],
            "persist_dict_nested": {
                "level1": {
                    "level2": {
                        "level3": "deep value"
                    }
                }
            }
        }
        
        temp_storage.save_process(process_name, test_data)
        loaded_data = temp_storage.load_process(process_name)
        
        assert loaded_data == test_data


if __name__ == "__main__":
    pytest.main([__file__])