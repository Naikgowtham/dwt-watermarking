import logging
import sys
import os
from datetime import datetime

def setup_logger(name, log_file=None, level=logging.DEBUG):
    if log_file is None:
        # Default log file path
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'all_time.log')
        current_log = os.path.join(log_dir, 'current_session.log')
        # Clear current session log at startup
        with open(current_log, 'w') as f:
            f.write("")
    else:
        current_log = None

    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')

    # File handler for all_time.log
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # File handler for current_session.log
    handlers = [file_handler]
    if current_log:
        file_handler_current = logging.FileHandler(current_log)
        file_handler_current.setFormatter(formatter)
        handlers.append(file_handler_current)

    # Console handler
    console_handler = logging.StreamHandler(sys.__stdout__)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []  # Remove any existing handlers
    for h in handlers:
        logger.addHandler(h)
    logger.propagate = False

    # Redirect print and uncaught exceptions to logger
    class StreamToLogger:
        def __init__(self, logger, level):
            self.logger = logger
            self.level = level
        def write(self, message):
            message = message.rstrip()
            if message:
                self.logger.log(self.level, message)
        def flush(self):
            pass

    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)

    # Redirect uncaught exceptions to logger
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception

    return logger
