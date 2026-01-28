from flask import Blueprint
from config import ENVIRONMENT

# This will be passed from app.py
_db = None

def set_db(db_instance):
    global _db
    _db = db_instance

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        _db.get_all_users()
        return {
            'status': 'healthy',
            'environment': ENVIRONMENT,
            'database': 'connected'
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'environment': ENVIRONMENT,
            'database': 'disconnected',
            'error': str(e)
        }, 500
