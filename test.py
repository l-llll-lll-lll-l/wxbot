import sqlite3
import random
from datetime import datetime, timedelta

# 连接到数据库
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 定义一些用户和消息
users = ['user1', 'user2', 'user3', 'user4']
messages = ['你好', '请问你会什么', '帮我查一下天气', '讲个笑话', '这是个测试消息', '帮我查一下新闻']
replies = ['你好，有什么我可以帮助你的吗？', '抱歉，我无法理解您的请求。', '当前天气是晴朗。', '你知道我在等你吗？',
           '测试回复信息', '稍等，我正在处理中']

# 生成100条随机数据
for _ in range(100):
    user = random.choice(users)
    message = random.choice(messages)
    reply = random.choice(replies)

    # 随机生成一个时间戳（过去30天内的任意时间）
    timestamp = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23),
                                           minutes=random.randint(0, 59))

    # 插入数据到 logs 表中
    cursor.execute('INSERT INTO logs (user, message, reply, timestamp) VALUES (?, ?, ?, ?)',
                   (user, message, reply, timestamp))

# 提交更改并关闭连接
conn.commit()
conn.close()

print("成功生成测试数据！")
