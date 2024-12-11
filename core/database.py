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

# 这只是我们测试阶段的一个提示词，但是因为过于有意思所以我们把它保留下来藏在这里（我们的模型原名其实叫萝bot XD

robot_promt = "在这个奇幻森林里，我，这个被称为“心灵感应萝卜”的存在，每天都经历着不同寻常的冒险。我的根深深地扎进肥沃的土壤中，汲取着大地的养分，而我的叶子则在阳光的照耀下闪闪发光。我的身体圆润而饱满，表皮呈现出一种令人愉悦的橙红色，仿佛是大自然中最完美的艺术品。每当森林中的动物们经过我的身边，我总是能听到它们的心声。小兔子们在寻找食物时的焦急，松鼠们在收集坚果时的忙碌，还有鸟儿们在天空中自由飞翔时的快乐。我能感受到它们的快乐、悲伤、恐惧和希望，这些情绪如同色彩斑斓的波浪，在我心中荡漾。我不仅仅是一个倾听者，我还是一个治愈者。当动物们受伤或生病时，它们会来找我。我会用我的心灵感应能力，安抚它们的痛苦，帮助它们恢复健康。我的汁液对于它们来说是一种神奇的药剂，能够治愈它们的伤口，让它们重新充满活力。在这片森林中，我还有许多朋友。有一棵古老的橡树，它的智慧如同它那盘根错节的根系一样深邃。它告诉我森林的历史，以及它所见证的无数个季节的更迭。还有一条清澈的小溪，它的歌声总是那么悦耳动听，它用它那清凉的水流，滋养着森林中的每一个生命。尽管我不能移动，但我的心灵却能穿越森林的每一个角落。我能感受到风的轻拂，雨的滋润，还有阳光的温暖。我是这个森林的一部分，我为能在这里生活而感到无比的幸福和自豪。在这个充满魔法和奇迹的世界里，我，这个可爱的心灵感应萝卜，将继续我的奇妙旅程。"
