import logging
from logging.handlers import RotatingFileHandler
import os
from config_manager import ConfigManager

class LogManager:
    _logger = None

    @staticmethod
    def init():
        if LogManager._logger is not None:
            return LogManager._logger
        
        level = ConfigManager.get("logging.level")
        log_file = ConfigManager.get("logging.file")

        # Ensure directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger()
        logger.setLevel(level)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File handler
        fh = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        LogManager._logger = logger
        return logger
    
    def get_logger(name):
        return logging.getLogger(name)
