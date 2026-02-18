import logging
import json
import datetime
import sys

class JSONFormatter(logging.Formatter):
    """
    Custom JSON Formatter for structured logging.
    """
    def format(self, record):
        # Base fields as requested by the user
        log_data = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "event": getattr(record, "event", "app_event"),
            "level": record.levelname,
            "message": record.getMessage()
        }
        
        # Add requested context fields if they exist
        if hasattr(record, "username"):
            log_data["username"] = record.username
        if hasattr(record, "email"):
            log_data["email"] = record.email
        if hasattr(record, "ip"):
            log_data["ip"] = record.ip
            
        # Optional: Add extra info for non-event logs
        if not hasattr(record, "event"):
            log_data.update({
                "logger": record.name,
                "module": record.module
            })
            
        # For error logs, include traceback if available
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)

def setup_logging(app):
    """
    Configures the Flask app logger to use JSON formatting and output to STDOUT.
    """
    # Remove existing handlers
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    # Create StreamHandler for STDOUT
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(JSONFormatter())
    
    app.logger.addHandler(stdout_handler)
    app.logger.setLevel(logging.INFO)
    
    # Prevent propagation to parent loggers (like gunicorn's error logger)
    # to avoid duplicate logs in some configurations
    app.logger.propagate = False
    
    app.logger.info('Flask Two-Tier App JSON logging initialized')
