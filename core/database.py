import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """创建数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                time TEXT,
                sender TEXT,
                receiver TEXT,
                content TEXT,
                msg_type TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_message(self, time, sender, receiver, content, msg_type):
        """保存消息到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (time, sender, receiver, content, msg_type) VALUES (?, ?, ?, ?, ?)
        ''', (time, sender, receiver, content, msg_type))
        conn.commit()
        conn.close()
