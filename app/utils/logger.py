import os
import logging
import traceback
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler

class AppLogger:
    def __init__(self):
        log_dir = os.path.join(os.path.dirname(__file__), "../logs")  
        os.makedirs(log_dir, exist_ok=True) 
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log") 

        handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
        )
        handler.suffix = "%Y-%m-%d"
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)

        logger = logging.getLogger("AppLogger")
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            logger.addHandler(handler)

        self._logger = logger

        self.delete_old_logs(log_dir)

    def get(self):
        return self._logger

    @staticmethod
    def delete_old_logs(log_dir):
        """Deletes log files older than 7 days."""
        seven_days_ago = datetime.today() - timedelta(days=7)
        for log_file in os.listdir(log_dir):
            file_path = os.path.join(log_dir, log_file)
            if os.path.isfile(file_path) and log_file.endswith(".log"):
                try:
                    file_date = datetime.strptime(log_file[:-4], "%Y-%m-%d")
                    if file_date < seven_days_ago:
                        os.remove(file_path)
                except ValueError:
                    continue  

logger = AppLogger().get()

def log_success(message):
    """Logs a success message with the exact file and line number."""
    stack = traceback.extract_stack()
    file_name, line_number, _, _ = stack[-2]  
    logger.info(f"SUCCESS: {message} - [File: {file_name}, Line: {line_number}]")

def log_error(message, exception=None):
    """Logs an error message with full traceback details."""
    if exception:
        tb_info = traceback.extract_tb(exception.__traceback__)
        if tb_info:
            file_name, line_number, _, _ = tb_info[-1]  
            logger.error(
                f"ERROR: {message} - Exception: {type(exception).__name__}: {exception} "
                f"- [File: {file_name}, Line: {line_number}]"
            )
        else:
            logger.error(f"ERROR: {message} - Exception: {type(exception).__name__}: {exception}")
    else:
        stack = traceback.extract_stack()
        file_name, line_number, _, _ = stack[-2]  
        logger.error(f"ERROR: {message} - [File: {file_name}, Line: {line_number}]")
def log_debug(message):
    """Logs a debug message with the exact file and line number."""
    stack = traceback.extract_stack()
    file_name, line_number, _, _ = stack[-2]  
    logger.debug(f"DEBUG: {message} - [File: {file_name}, Line: {line_number}]")
def log_info(message):
    """Logs an info message with the exact file and line number."""
    stack = traceback.extract_stack()
    file_name, line_number, _, _ = stack[-2]  
    logger.info(f"INFO: {message} - [File: {file_name}, Line: {line_number}]")