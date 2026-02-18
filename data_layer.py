import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional
import contextlib

class DataLayer:
    """Data layer for handling all database operations with PostgreSQL"""
    
    def __init__(self, host: str = 'localhost', database: str = 'userdb', 
                 user: str = 'postgres', password: str = 'postgres', port: int = 5432):
        """Initialize the data layer with a PostgreSQL connection pool"""
        self.connection_pool = pool.SimpleConnectionPool(
            1, 20,
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        self._init_database()

    @contextlib.contextmanager
    def _get_connection(self):
        """Get a connection from the pool and release it back."""
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)
    
    def _init_database(self):
        """Initialize the database schema"""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL UNIQUE,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        address VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    ALTER TABLE users ADD COLUMN IF NOT EXISTS address VARCHAR(255);
                ''')
                conn.commit()
    
    def add_user(self, name: str, email: str, address: str) -> int:
        """Add a new user to the database"""
        user_id = None
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users (name, email, address) VALUES (%s, %s, %s) RETURNING id',
                    (name, email, address)
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
        return user_id
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get a single user by ID"""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
                row = cursor.fetchone()
        
        return dict(row) if row else None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users from the database"""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
                rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def update_user(self, user_id: int, name: str, email: str, address: str) -> bool:
        """Update an existing user"""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE users SET name = %s, email = %s, address = %s WHERE id = %s',
                    (name, email, address, user_id)
                )
                affected = cursor.rowcount
                conn.commit()
        
        return affected > 0
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database"""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
                affected = cursor.rowcount
                conn.commit()
        
        return affected > 0

