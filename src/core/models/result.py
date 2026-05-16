from typing import Generic, TypeVar, Optional, Any

T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    """
    A generic Result class for encapsulating success and failure outcomes.
    
    Used In: Application-wide for error handling without exceptions.
    """
    
    def __init__(self, is_success: bool, value: Optional[T] = None, error: Optional[E] = None) -> None:
        self.is_success = is_success
        self.value = value
        self.error = error

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        """Creates a successful result."""
        return cls(is_success=True, value=value)

    @classmethod
    def fail(cls, error: E) -> 'Result[T, E]':
        """Creates a failed result."""
        return cls(is_success=False, error=error)
