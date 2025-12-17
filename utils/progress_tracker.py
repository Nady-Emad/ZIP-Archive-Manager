"""
Progress Tracker Module
Handles progress tracking and callbacks for operations
"""

from typing import Optional, Callable
import time


class ProgressTracker:
    """Tracks and reports progress of operations"""
    
    def __init__(self, callback: Optional[Callable] = None):
        """
        Initialize progress tracker
        
        Args:
            callback: Optional callback function(current, total, message)
        """
        self.callback = callback
        self.total = 0
        self.current = 0
        self.message = ""
        self.start_time = None
        self.is_active = False
    
    def start(self, total: int, message: str = "Starting..."):
        """
        Start tracking progress
        
        Args:
            total: Total number of items to process
            message: Initial status message
        """
        self.total = total
        self.current = 0
        self.message = message
        self.start_time = time.time()
        self.is_active = True
        self._notify(0, message)
    
    def update(self, current: int, message: str = ""):
        """
        Update progress
        
        Args:
            current: Current progress count
            message: Status message
        """
        if not self.is_active:
            return
        
        self.current = current
        if message:
            self.message = message
        
        self._notify(current, message)
    
    def increment(self, message: str = ""):
        """
        Increment progress by one
        
        Args:
            message: Status message
        """
        self.update(self.current + 1, message)
    
    def complete(self, message: str = "Complete"):
        """
        Mark operation as complete
        
        Args:
            message: Completion message
        """
        self.current = self.total
        self.message = message
        self.is_active = False
        self._notify(self.total, message)
    
    def error(self, message: str):
        """
        Report an error
        
        Args:
            message: Error message
        """
        self.is_active = False
        self._notify(-1, f"ERROR: {message}")
    
    def get_progress_percentage(self) -> float:
        """Get current progress as percentage"""
        if self.total == 0:
            return 0.0
        return (self.current / self.total) * 100
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since start in seconds"""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
    
    def get_estimated_time_remaining(self) -> Optional[float]:
        """Get estimated time remaining in seconds"""
        if not self.is_active or self.current == 0:
            return None
        
        elapsed = self.get_elapsed_time()
        rate = self.current / elapsed
        remaining = self.total - self.current
        
        return remaining / rate if rate > 0 else None
    
    def _notify(self, current: int, message: str):
        """
        Notify callback of progress update
        
        Args:
            current: Current progress
            message: Status message
        """
        if self.callback:
            try:
                self.callback(current, self.total, message)
            except Exception:
                # Don't let callback errors break the operation
                pass


class ConsoleProgressTracker(ProgressTracker):
    """Progress tracker that prints to console"""
    
    def __init__(self):
        """Initialize console progress tracker"""
        super().__init__(callback=self._console_callback)
    
    def _console_callback(self, current: int, total: int, message: str):
        """Print progress to console"""
        if current == -1:
            # Error
            print(f"\n❌ {message}")
        elif current >= total and total > 0:
            # Complete
            elapsed = self.get_elapsed_time()
            print(f"\n✓ {message} (took {elapsed:.2f}s)")
        else:
            # Progress
            if total > 0:
                percentage = (current / total) * 100
                bar_length = 40
                filled = int(bar_length * current / total)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f"\r[{bar}] {percentage:.1f}% - {message}", end='', flush=True)
            else:
                print(f"\r{message}", end='', flush=True)
