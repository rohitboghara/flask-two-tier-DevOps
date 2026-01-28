"""
config.py - Application Configuration
Loads settings from environment variables (.env file)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'userdb'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'port': int(os.getenv('DB_PORT', 5432))
}

# Flask Application Configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key-change-this')
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
HOST = os.getenv('FLASK_HOST', '0.0.0.0')
PORT = int(os.getenv('FLASK_PORT', 5000))

# Application Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


# Additional Configuration based on Environment
if ENVIRONMENT == 'production':
    DEBUG = False
    # Add production-specific settings here
elif ENVIRONMENT == 'testing':
    DEBUG = True
    DATABASE_CONFIG['database'] = 'userdb_test'
    # Add testing-specific settings here

# Database Connection String (if needed)
DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Print configuration on load (for debugging - remove in production)
if DEBUG:
    print("=" * 50)
    print("Configuration Loaded:")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Database Host: {DATABASE_CONFIG['host']}")
    print(f"Database Name: {DATABASE_CONFIG['database']}")
    print(f"Database User: {DATABASE_CONFIG['user']}")
    print(f"Database Port: {DATABASE_CONFIG['port']}")
    print(f"Flask Host: {HOST}")
    print(f"Flask Port: {PORT}")
    print(f"Debug Mode: {DEBUG}")
    print("=" * 50)
