import logging
import sys

def setup_logging():
    """Configures structured logging for the application."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    # If handlers are already configured, do nothing
    if logger.hasHandlers():
        return logger

    # Configure a stream handler to output to the console
    handler = logging.StreamHandler(sys.stdout)
    
    # Set a professional format for the log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)
    
    return logger

# Create a logger instance for modules to import
log = setup_logging()
