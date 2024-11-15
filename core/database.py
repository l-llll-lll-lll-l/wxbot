import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        """创建数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                time TEXT,
                sender TEXT,
                receiver TEXT,
                content TEXT,
                msg_type TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                prompts TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_users (
                bot_name TEXT,
                user_name TEXT,
                PRIMARY KEY (bot_name, user_name)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE
            )
        ''')
        conn.commit()
        conn.close()
        
    def get_all_users(self):
        """获取所有用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return [user[1] for user in users]
    
    def get_logs_basic(self, **kwargs):
        """根据条件获取消息列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 构建基础查询语句
        query = 'SELECT * FROM logs'
        
        # 构建条件语句
        conditions = []
        params = []
        for key, value in kwargs.items():
            conditions.append(f'{key} = ?')
            params.append(value)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        cursor.execute(query, tuple(params))
        messages = cursor.fetchall()
        conn.close()
        return [{'id': msg[0], 'time': msg[1], 'sender': msg[2], 'receiver': msg[3], 'content': msg[4], 'msg_type': msg[5]} for msg in messages]

    def get_logs_order_by_time(self, **kwargs):
        """根据条件获取消息列表，并按时间排序"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 构建基础查询语句
        query = 'SELECT * FROM logs'
        
        # 构建条件语句
        conditions = []
        params = []
        for key, value in kwargs.items():
            conditions.append(f'{key} = ?')
            params.append(value)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY time'
        
        cursor.execute(query, tuple(params))
        messages = cursor.fetchall()
        conn.close()
        return [{'id': msg[0], 'time': msg[1], 'sender': msg[2], 'receiver': msg[3], 'content': msg[4], 'msg_type': msg[5]} for msg in messages]

    def get_users_for_bot(self, bot_name):
        """获取某个机器人负责的所有用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT user_name FROM bot_users WHERE bot_name = ?', (bot_name,))
        users = cursor.fetchall()
        conn.close()
        return [user[0] for user in users]

    def get_bot_for_user(self, user_name):
        """获取某个用户的对应的机器人（一个用户只对应一个机器人）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT bot_name FROM bot_users WHERE user_name = ?', (user_name,))
        bot = cursor.fetchone()
        conn.close()
        return bot[0] if bot else None

    def remove_user_from_bot(self, bot_name, user_name):
        """从机器人的监听列表中移除用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bot_users WHERE bot_name = ? AND user_name = ?', (bot_name, user_name))
        conn.commit()
        conn.close()

    def remove_user_whatever_bot(self, user_name):
        """从所有机器人的监听列表中移除用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bot_users WHERE user_name = ?', (user_name,))
        conn.commit()
        conn.close()

    def save_log(self, time, sender, receiver, content, msg_type):
        """保存消息到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (time, sender, receiver, content, msg_type) VALUES (?, ?, ?, ?, ?)
        ''', (time, sender, receiver, content, msg_type))
        conn.commit()
        conn.close()
    
    def save_user(self, username):
        """保存用户到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        conn.close()
        
    def reset_users_with_list(self, users):
        """重置用户表并用一个列表覆写"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users')
        for user in users:
            cursor.execute('INSERT INTO users (username) VALUES (?)', (user,))
        conn.commit()
        conn.close()
        
    def save_bot(self, name, prompts):
        """保存机器人信息到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bots (name, prompts) VALUES (?, ?)
        ''', (name, prompts))
        conn.commit()
        conn.close()

    def get_bot(self, name):
        """根据名称获取机器人信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bots WHERE name = ?', (name,))
        bot = cursor.fetchone()
        conn.close()
        if bot:
            return {'id': bot[0], 'name': bot[1], 'prompts': bot[2]}
        return None

    def update_bot(self, name, prompts):
        """更新机器人信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE bots SET prompts = ? WHERE name = ?', (prompts, name))
        conn.commit()
        conn.close()
        
    def delete_bot(self, name):
        """删除机器人信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bots WHERE name = ?', (name,))
        conn.commit()
        conn.close()

    def list_bots(self):
        """列出所有机器人信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bots')
        bots = cursor.fetchall()
        conn.close()
        return [{'id': bot[0], 'name': bot[1], 'prompts': bot[2]} for bot in bots]
    
    def assign_user_to_bot(self, bot_name, user_name):
        """将用户分配给机器人"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bot_users (bot_name, user_name) VALUES (?, ?)
        ''', (bot_name, user_name))
        conn.commit()
        conn.close()