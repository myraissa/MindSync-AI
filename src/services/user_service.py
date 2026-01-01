# src/services/user_service.py

import sqlite3
from datetime import datetime
import uuid

class UserService:
    """
    Manage users and conversation limits
    """
    
    def __init__(self, db_path='data/users.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        Create database tables
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                daily_conversations INTEGER DEFAULT 0,
                last_reset DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                user_id TEXT,
                message TEXT,
                emotion TEXT,
                intent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, name: str) -> str:
        """
        Create new user
        """
        user_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (user_id, name)
            VALUES (?, ?)
        ''', (user_id, name))
        
        conn.commit()
        conn.close()
        
        return user_id
    
    def check_daily_limit(self, user_id: str) -> bool:
        """
        Check if user reached 5 conversation limit
        
        Returns True if limit NOT reached
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Reset counter if new day
        cursor.execute('''
            UPDATE users
            SET daily_conversations = 0,
                last_reset = CURRENT_DATE
            WHERE user_id = ? AND last_reset < CURRENT_DATE
        ''', (user_id,))
        
        # Check limit
        cursor.execute('''
            SELECT daily_conversations
            FROM users
            WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0] < 5  # FREE limit = 5 conversations
        
        return True
    
    def increment_conversation_count(self, user_id: str):
        """
        Increment user's daily conversation count
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET daily_conversations = daily_conversations + 1
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
