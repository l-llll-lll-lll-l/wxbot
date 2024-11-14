from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session, send_file
import sqlite3
import time
import random
import csv

app = Flask(__name__)


# 初始化数据库并创建 logs 表和 robot_user_relations 表
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # 创建日志表
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT NOT NULL,
                        message TEXT NOT NULL,
                        reply TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    # 创建机器人和用户的关系表
    cursor.execute('''CREATE TABLE IF NOT EXISTS robot_user_relations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        robot TEXT NOT NULL,
                        user TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()


# 调用初始化函数
init_db()

# 用户的回复规则
user_reply_rules = {}
default_reply_rule = {'keyword': '你好', 'response': '你好，有什么我可以帮助你的吗？'}


# 加载用户
def load_users_from_file():
    with open('users.txt', 'r', encoding='utf-8') as file:
        users = file.readlines()
    return [user.strip() for user in users]

def add_log(user, message, reply):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (user, message, reply) VALUES (?, ?, ?)', (user, message, reply))
    conn.commit()
    conn.close()

def robot_message(input_text):
    user_id = session.get('user_id')
    for rule in user_reply_rules.get(user_id, []):
        if rule['keyword'] in input_text:
            reply = rule['response']
            add_log(user_id, input_text, reply)
            return reply
    reply = "抱歉，我无法理解您的请求。"
    add_log(user_id, input_text, reply)
    return reply

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/reply-settings', methods=['GET', 'POST'])
def reply_settings():
    users = load_users_from_file()

    for user in users:
        if user not in user_reply_rules:
            user_reply_rules[user] = []

    if request.method == 'POST':
        selected_user = request.form.get('selected_user')
        keyword = request.form.get('keyword')

        if selected_user and keyword:
            user_reply_rules[selected_user].append({'keyword': keyword, 'response': "抱歉，我无法理解您的请求。"})
            flash('回复规则已添加', 'success')
        else:
            flash('请填写所有字段', 'error')

    return render_template('reply_settings.html', users=user_reply_rules.keys(), user_reply_rules=user_reply_rules)


@app.route('/logs')
def logs_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT user FROM logs')
    users = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT timestamp, user, message, reply FROM logs ORDER BY timestamp DESC')
    logs = cursor.fetchall()
    conn.close()

    return render_template('logs.html', users=users, logs=logs)


@app.route('/export_logs')
def export_logs():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, user, message, reply FROM logs')
    logs = cursor.fetchall()
    conn.close()

    with open('logs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'User', 'Message', 'Reply'])
        writer.writerows(logs)

    return send_file('logs.csv', as_attachment=True)


# 更新机器人和用户关联的路由
@app.route('/robot-management', methods=['GET', 'POST'])
def robot_management():
    # 机器人列表和用户列表
    robots = ["Robot1", "Robot2", "Robot3"]
    users = load_users_from_file()

    if request.method == 'POST':
        # 获取机器人和用户的关联信息
        data = request.get_json()
        selected_robot = data.get('robot')
        selected_users = data.get('users')

        # 清除旧的关联
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM robot_user_relations WHERE robot = ?', (selected_robot,))

        # 插入新的关联
        for user in selected_users:
            cursor.execute('INSERT INTO robot_user_relations (robot, user) VALUES (?, ?)', (selected_robot, user))
        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200

    return render_template('robot_management.html', robots=robots, users=users)

if __name__ == '__main__':
    app.run(debug=True)
