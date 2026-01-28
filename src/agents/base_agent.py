"""
Base Agent Module

This module provides the abstract base class for all agents
in the RM-AgenticAI-LangGraph system.

All agents inherit from BaseAgent and implement:
- _execute(): Primary execution logic
- _fallback(): Fallback logic when primary fails
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic
from datetime import datetime
from dataclasses import dataclass
import asyncio
from functools import wraps

# Type variable for result types
T = TypeVar('T')


@dataclass
class ExecutionResult(Generic[T]):
    """
    Standard result wrapper for agent execution.
    
    Attributes:
        result: The actual computation result
        success: Whether execution succeeded
        fallback_used: Whether fallback logic was used
        duration_ms: Execution duration in milliseconds
        error_message: Error message if failed
    """
    result: Optional[T]
    success: bool
    fallback_used: bool = False
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    agent_name: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "result": self.result,
            "success": self.success,
            "fallback_used": self.fallback_used,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "agent_name": self.agent_name
        }


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    
    Provides:
    - Standard execution flow with error handling
    - Automatic metrics collection
    - Logging integration
    - Fallback mechanism
    
    Usage:
        class MyAgent(BaseAgent):
            async def _execute(self, **kwargs):
                # Primary logic
                return result
            
            def _fallback(self, **kwargs):
                # Fallback logic
                return default_result
    """
    
    def __init__(self, name: str):
        """
        Initialize the agent.
        
        Args:
            name: Human-readable agent name for logging
        """
        self.name = name
        self._start_time: Optional[datetime] = None
        self._execution_count = 0
        self._success_count = 0
        self._fallback_count = 0
    
    @abstractmethod
    async def _execute(self, **kwargs) -> Any:
        """
        Core execution logic - must be implemented by subclasses.
        
        This method contains the primary business logic of the agent.
        It should raise exceptions on failure, which will trigger
        the fallback mechanism.
        
        Args:
            **kwargs: Agent-specific input parameters
            
        Returns:
            Agent-specific result object
            
        Raises:
            Any exception will trigger fallback
        """
        pass
    
    @abstractmethod
    def _fallback(self, **kwargs) -> Any:
        """
        Fallback logic - must be implemented by subclasses.
        
        This method provides a guaranteed result when primary
        execution fails. It should not raise exceptions.
        
        Args:
            **kwargs: Same parameters as _execute
            
        Returns:
            Safe default result
        """
        pass
    
    async def execute(self, **kwargs) -> ExecutionResult:
        """
        Execute the agent with full error handling and metrics.
        
        This is the main entry point for agent execution.
        It handles:
        1. Timing and metrics
        2. Error handling
        3. Fallback invocation
        4. Result wrapping
        
        Args:
            **kwargs: Parameters passed to _execute and _fallback
            
        Returns:
            ExecutionResult containing the result and metadata
        """
        self._start_time = datetime.now()
        self._execution_count += 1
        
        self._log(f"Starting execution with inputs: {list(kwargs.keys())}")
        
        try:
            # Primary execution
            result = await self._execute(**kwargs)
            self._success_count += 1
            
            duration = self._get_duration()
            self._log(f"Execution completed successfully in {duration:.2f}ms")
            
            return ExecutionResult(
                result=result,
                success=True,
                fallback_used=False,
                duration_ms=duration,
                agent_name=self.name
            )
            
        except Exception as e:
            self._log(f"Primary execution failed: {e}, attempting fallback")
            
            try:
                # Fallback execution
                result = self._fallback(**kwargs)
                self._fallback_count += 1
                
                duration = self._get_duration()
                self._log(f"Fallback completed in {duration:.2f}ms")
                
                return ExecutionResult(
                    result=result,
                    success=True,
                    fallback_used=True,
                    duration_ms=duration,
                    agent_name=self.name
                )
                
            except Exception as fallback_error:
                duration = self._get_duration()
                self._log(f"Fallback also failed: {fallback_error}")
                
                return ExecutionResult(
                    result=None,
                    success=False,
                    fallback_used=True,
                    duration_ms=duration,
                    error_message=str(fallback_error),
                    agent_name=self.name
                )
    
    def execute_sync(self, **kwargs) -> ExecutionResult:
        """
        Synchronous wrapper for execute().
        
        Args:
            **kwargs: Parameters passed to execute
            
        Returns:
            ExecutionResult
        """
        return asyncio.run(self.execute(**kwargs))
    
    def _get_duration(self) -> float:
        """Calculate execution duration in milliseconds."""
        if self._start_time:
            return (datetime.now() - self._start_time).total_seconds() * 1000
        return 0.0
    
    def _log(self, message: str) -> None:
        """
        Log a message with agent context.
        
        In production, this would integrate with Loguru or similar.
        """
        print(f"[{self.name}] {message}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get agent performance metrics.
        
        Returns:
            Dictionary containing execution statistics
        """
        total = self._execution_count
        return {
            "agent_name": self.name,
            "total_executions": total,
            "success_count": self._success_count,
            "fallback_count": self._fallback_count,
            "success_rate": self._success_count / total if total > 0 else 0,
            "fallback_rate": self._fallback_count / total if total > 0 else 0
        }
    
    def reset_metrics(self) -> None:
        """Reset all metrics counters."""
        self._execution_count = 0
        self._success_count = 0
        self._fallback_count = 0


# =============================================================================
# DECORATORS FOR AGENT METHODS
# =============================================================================

def with_retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to add retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay after each retry
        
    Example:
        @with_retry(max_retries=3)
        async def call_external_api():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    
                    if attempt < max_retries - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_error
        return wrapper
    return decorator


def with_timeout(seconds: float):
    """
    Decorator to add timeout to async functions.
    
    Args:
        seconds: Maximum execution time in seconds
        
    Example:
        @with_timeout(30.0)
        async def long_running_operation():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                raise TimeoutError(f"Operation timed out after {seconds} seconds")
        return wrapper
    return decorator


def with_validation(validator_func):
    """
    Decorator to validate inputs before execution.
    
    Args:
        validator_func: Function that takes **kwargs and returns bool
        
    Example:
        @with_validation(lambda **kw: 'data' in kw)
        async def process_data(data):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not validator_func(**kwargs):
                raise ValueError("Input validation failed")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
