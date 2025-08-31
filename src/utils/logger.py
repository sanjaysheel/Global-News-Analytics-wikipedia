"""
Centralized logging utility for the Wikipedia scraper project.
Provides consistent logging across all modules with Databricks compatibility.
"""
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime
import inspect

# Global logger cache
_loggers = {}

class DatabricksLogger:
    """Custom logger that works well in both Databricks and local environments"""
    
    def __init__(self, name: str, level: str = "INFO", log_file: Optional[str] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        
        # Set log level
        self.set_level(level)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]'
        )
        simple_formatter = logging.Formatter('%(levelname)s - %(message)s')
        
        # Console handler (always available)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            self._setup_file_handler(log_file, detailed_formatter)
        
        # Databricks-specific optimizations
        self._setup_databricks_compatibility()
        
        # Prevent propagation to avoid duplicate logs
        self.logger.propagate = False
    
    def set_level(self, level: str) -> None:
        """Set logging level"""
        level = level.upper()
        if level == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif level == "INFO":
            self.logger.setLevel(logging.INFO)
        elif level == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif level == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.INFO)
    
    def _setup_file_handler(self, log_file: str, formatter: logging.Formatter) -> None:
        """Setup file handler with proper path handling for Databricks"""
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            self.logger.warning(f"Could not setup file logging to {log_file}: {e}")
    
    def _setup_databricks_compatibility(self) -> None:
        """Setup Databricks-specific logging optimizations"""
        try:
            # Check if we're running in Databricks
            dbutils_available = True
            try:
                from pyspark.dbutils import DBUtils  # noqa: F401
            except ImportError:
                dbutils_available = False
            
            if dbutils_available:
                # In Databricks, we might want to use display() for important messages
                self._databricks_display = self._create_databricks_display_function()
        except:
            pass  # Silently fail if Databricks-specific setup fails
    
    def _create_databricks_display_function(self):
        """Create display function for Databricks if available"""
        try:
            from IPython.display import display, HTML
            def display_html(message, level="info"):
                color = {
                    "info": "blue",
                    "warning": "orange",
                    "error": "red",
                    "success": "green"
                }.get(level, "black")
                
                html = f'<div style="color: {color}; padding: 10px; border-left: 4px solid {color}; margin: 5px 0;">{message}</div>'
                display(HTML(html))
            
            return display_html
        except:
            return None
    
    def debug(self, message: str, extra: Optional[Dict] = None) -> None:
        """Log debug message"""
        self.logger.debug(self._format_message(message), extra=extra)
    
    def info(self, message: str, extra: Optional[Dict] = None) -> None:
        """Log info message"""
        self.logger.info(self._format_message(message), extra=extra)
        self._databricks_display_info(message)
    
    def warning(self, message: str, extra: Optional[Dict] = None) -> None:
        """Log warning message"""
        self.logger.warning(self._format_message(message), extra=extra)
        self._databricks_display_warning(message)
    
    def error(self, message: str, extra: Optional[Dict] = None) -> None:
        """Log error message"""
        self.logger.error(self._format_message(message), extra=extra)
        self._databricks_display_error(message)
    
    def critical(self, message: str, extra: Optional[Dict] = None) -> None:
        """Log critical message"""
        self.logger.critical(self._format_message(message), extra=extra)
        self._databricks_display_error(message)
    
    def exception(self, message: str, exc_info: bool = True) -> None:
        """Log exception with traceback"""
        self.logger.exception(self._format_message(message), exc_info=exc_info)
        self._databricks_display_error(f"{message} - Check logs for details")
    
    def _format_message(self, message: str) -> str:
        """Format log message with additional context"""
        # Add calling function name for better debugging
        try:
            frame = inspect.currentframe().f_back.f_back
            func_name = frame.f_code.co_name
            lineno = frame.f_lineno
            return f"[{func_name}:{lineno}] {message}"
        except:
            return message
    
    def _databricks_display_info(self, message: str) -> None:
        """Display info message in Databricks notebook"""
        if hasattr(self, '_databricks_display') and self._databricks_display:
            self._databricks_display(message, "info")
    
    def _databricks_display_warning(self, message: str) -> None:
        """Display warning message in Databricks notebook"""
        if hasattr(self, '_databricks_display') and self._databricks_display:
            self._databricks_display(message, "warning")
    
    def _databricks_display_error(self, message: str) -> None:
        """Display error message in Databricks notebook"""
        if hasattr(self, '_databricks_display') and self._databricks_display:
            self._databricks_display(message, "error")
    
    def log_performance(self, operation: str, duration: float, details: Optional[Dict] = None) -> None:
        """Log performance metrics in structured format"""
        perf_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "duration_seconds": round(duration, 3),
            "details": details or {}
        }
        
        self.info(f"PERFORMANCE: {json.dumps(perf_data)}")
    
    def log_scraping_metrics(self, topic: str, success: bool, duration: float, 
                           content_length: int = 0) -> None:
        """Log structured scraping metrics"""
        metrics = {
            "topic": topic,
            "success": success,
            "duration_seconds": round(duration, 3),
            "content_length": content_length,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.info(f"SCRAPING_METRICS: {json.dumps(metrics)}")

def get_logger(name: str = None, config: Optional[Dict] = None) -> DatabricksLogger:
    """
    Get or create a logger instance with consistent configuration.
    
    Args:
        name: Logger name (usually __name__)
        config: Optional configuration dictionary
    
    Returns:
        DatabricksLogger instance
    """
    if name is None:
        # Get caller's module name
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')
    
    if name in _loggers:
        return _loggers[name]
    
    # Default configuration
    default_config = {
        "level": "INFO",
        "log_file": None
    }
    
    # Merge with provided config
    if config:
        default_config.update(config)
    
    # Create new logger
    logger = DatabricksLogger(
        name=name,
        level=default_config["level"],
        log_file=default_config["log_file"]
    )
    
    _loggers[name] = logger
    return logger

def setup_root_logger(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup root logger configuration"""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    root_logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to setup file logging: {e}")

# Example usage and quick setup function
def quick_setup(module_name: str, level: str = "INFO") -> DatabricksLogger:
    """Quick setup for a logger with sensible defaults"""
    return get_logger(module_name, {"level": level})

# Initialize when module is imported
setup_root_logger()