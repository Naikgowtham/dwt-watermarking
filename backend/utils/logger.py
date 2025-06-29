import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Log file paths
    all_time_log = os.path.join(log_dir, 'all_time.log')
    current_log = os.path.join(log_dir, 'current_session.log')

    # Reset current session log
    with open(current_log, 'w') as f:
        f.write("")  # Clear contents

    # Append session header to all_time.log
    with open(all_time_log, 'a') as f:
        f.write(f"\n\n========== New Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==========\n")

    # Define log format
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')

    # Get logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Prevent duplicate handlers on multiple imports
    if not logger.handlers:

        # Handler for current session
        file_handler_current = logging.FileHandler(current_log)
        file_handler_current.setLevel(logging.DEBUG)
        file_handler_current.setFormatter(formatter)

        # Handler for all-time log
        file_handler_all = logging.FileHandler(all_time_log)
        file_handler_all.setLevel(logging.DEBUG)
        file_handler_all.setFormatter(formatter)

        # Console (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Attach handlers
        logger.addHandler(file_handler_current)
        logger.addHandler(file_handler_all)
        logger.addHandler(console_handler)

    return logger
