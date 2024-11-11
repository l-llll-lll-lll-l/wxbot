from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session, send_file
import sqlite3
import pyqrcode
import time
import random
import json
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 初始化数据库并创建 logs 表
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT NOT NULL,
                        message TEXT NOT NULL,
                        reply TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

# 调用初始化函数
init_db()

# 存储二维码和用户状态
qrcode_data = {}
qr_expiry_time = 300  # 二维码过期时间（秒）

# 用户的回复规则
user_reply_rules = {}
default_reply_rule = {'keyword': '你好', 'response': '你好，有什么我可以帮助你的吗？'}

# 加载用户
def load_users_from_file():
    with open('users.txt', 'r', encoding='utf-8') as file:
        users = file.readlines()
    return [user.strip() for user in users]

def generate_qr_code(user_id):
    qr = pyqrcode.create(user_id)
    return qr.png_as_base64_str(scale=5)

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
def index():
    user_id = str(random.randint(1000, 9999))
    qr_code = generate_qr_code(user_id)
    qrcode_data[user_id] = {'qr_code': qr_code, 'timestamp': time.time(), 'logged_in': False}
    return render_template('login.html', qr_code=qr_code, user_id=user_id)

@app.route('/check_login/<user_id>', methods=['GET'])
def check_login(user_id):
    if user_id in qrcode_data:
        if time.time() - qrcode_data[user_id]['timestamp'] < qr_expiry_time:
            if qrcode_data[user_id]['logged_in']:
                return jsonify({'status': 'logged_in'})
            return jsonify({'status': 'valid'})
    return jsonify({'status': 'invalid'})

@app.route('/login/<user_id>', methods=['POST'])
def login(user_id):
    if user_id in qrcode_data:
        qrcode_data[user_id]['logged_in'] = True
        session['user_id'] = user_id
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', user_id=session['user_id'])

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

@app.route('/robot-management')
def robot_management():
    # Example list of robots for selection
    robots = ["Robot1", "Robot2", "Robot3"]
    return render_template('robot_management.html', robots=robots)

@app.route('/reply/<input_text>')
def get_reply(input_text):
    reply = robot_message(input_text)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
