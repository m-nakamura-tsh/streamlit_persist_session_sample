# Flexible data models for persistence layer
from typing import Any, Dict, List, Union

# Type definitions for JSON serializable data
type JsonSerializable = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
type ProcessData = Dict[str, JsonSerializable]

# Note: This module previously contained rigid dataclass models (ProcessState, ProcessStep, etc.)
# but has been simplified to support flexible dict-based data structures.
# This allows for dynamic data schemas without requiring model updates.
