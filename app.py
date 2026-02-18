"""
app.py - Flask Application with Environment Variables
Two-Tier Architecture - Presentation Layer
"""

from flask import Flask, render_template, flash
from flask_wtf.csrf import CSRFProtect
from data_layer import DataLayer
from config import DATABASE_CONFIG, SECRET_KEY, DEBUG, HOST, PORT, ENVIRONMENT
from prometheus_flask_exporter import PrometheusMetrics
import psutil
import threading
import time
from prometheus_client import Gauge
import traceback

# Import logging_config
from logging_config import setup_logging

# Import Blueprints
from routes.main_routes import main_bp
from routes.health_routes import health_bp

# Initialize Flask application
app = Flask(__name__)

# Setup logging
setup_logging(app)

app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)

# Initialize Prometheus Metrics
metrics = PrometheusMetrics(app)

# --- Custom System Metrics ---
# Define Prometheus Gauges for system metrics
cpu_usage_gauge = Gauge('system_cpu_usage_percent', 'Current CPU usage in percentage')
memory_usage_gauge = Gauge('system_memory_usage_percent', 'Current Memory usage in percentage')
disk_usage_gauge = Gauge('system_disk_usage_percent', 'Current Disk usage in percentage')

def collect_system_metrics():
    """Collects system-wide CPU, memory, and disk usage and updates Prometheus gauges."""
    cpu_usage_gauge.set(psutil.cpu_percent(interval=None))
    memory_usage_gauge.set(psutil.virtual_memory().percent)
    
    # Assuming we want to monitor the disk usage of the root partition
    disk_usage = psutil.disk_usage('/')
    disk_usage_gauge.set(disk_usage.percent)

def update_metrics_periodically():
    """Updates system metrics every 5 seconds."""
    while True:
        collect_system_metrics()
        time.sleep(5) # Update every 5 seconds

# Start the background thread for updating metrics
metrics_thread = threading.Thread(target=update_metrics_periodically, daemon=True)
metrics_thread.start()
# --- End Custom System Metrics ---

# Initialize data layer with PostgreSQL connection from environment variables
try:
    app.db = DataLayer(
        host=DATABASE_CONFIG['host'],
        database=DATABASE_CONFIG['database'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        port=DATABASE_CONFIG['port']
    )
    app.logger.info("Database connection established successfully!", extra={"event": "db_connected"})
except Exception as e:
    app.db = None
    app.logger.error(f"Database connection failed: {e}", extra={"event": "db_connection_failed"})
    app.logger.warning("Please check your .env file and database configuration. The application will start but database features will be unavailable.")


# Store csrf instance on app object
app.csrf = csrf

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(health_bp)

# Centralized Error Handler
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the full traceback for debugging
    app.logger.error(f"Unhandled Exception: {e}", extra={
        "event": "unhandled_exception",
        "exception": traceback.format_exc()
    })
    flash('An unexpected error occurred. Please try again later.', 'error')
    return render_template('index.html'), 500


if __name__ == '__main__':
    app.logger.info(f"Starting Flask application in {ENVIRONMENT} mode...", extra={
        "event": "app_startup",
        "environment": ENVIRONMENT,
        "host": HOST,
        "port": PORT
    })
    
    app.run(debug=DEBUG, host=HOST, port=PORT)
