"""Logging utilities for the application."""
import logging
from datetime import datetime
from pathlib import Path


class PhotogrammetryLogger:
    """Custom logger for photogrammetry operations."""
    
    def __init__(self, log_dir=None, log_level=logging.INFO):
        """
        Initialize logger.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.logger = logging.getLogger('PhotogrammetryGUI')
        self.logger.setLevel(log_level)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler (if log_dir specified)
        if log_dir:
            log_dir = Path(log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = log_dir / f'photogrammetry_{timestamp}.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_format = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
            
            self.log_file = log_file
        else:
            self.log_file = None
    
    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message."""
        self.logger.critical(message)
    
    def get_log_file(self):
        """Get path to log file."""
        return self.log_file


# Global logger instance
_global_logger = None


def get_logger(log_dir=None):
    """
    Get or create global logger instance.
    
    Args:
        log_dir: Directory for log files (only used on first call)
        
    Returns:
        PhotogrammetryLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = PhotogrammetryLogger(log_dir=log_dir)
    return _global_logger
