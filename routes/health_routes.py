from flask import Blueprint, current_app
from config import ENVIRONMENT

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Use a simpler query for health check
        with current_app.db._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
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
