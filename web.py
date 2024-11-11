from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
import pyqrcode
import time
import random
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪现消息的安全密钥

# 存储二维码和用户状态
qrcode_data = {}
qr_expiry_time = 300  # 二维码过期时间（秒）

# 用于存储每个用户的回复规则
user_reply_rules = {}

# 默认回复规则
default_reply_rule = {'keyword': '你好', 'response': '你好，有什么我可以帮助你的吗？'}

# 从文件加载用户
def load_users_from_file():
    with open('users.txt', 'r', encoding='utf-8') as file:
        users = file.readlines()
    return [user.strip() for user in users]

def generate_qr_code(user_id):
    qr = pyqrcode.create(user_id)
    return qr.png_as_base64_str(scale=5)

def robot_message(input_text):
    for rule in user_reply_rules.get(session.get('user_id'), []):
        if rule['keyword'] in input_text:
            return rule['response']
    return "抱歉，我无法理解您的请求。"

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
        qrcode_data[user_id]['logged_in'] = True  # 设置用户为已登录
        session['user_id'] = user_id  # 在会话中存储用户ID
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

    # 初始化用户的回复规则
    for user in users:
        if user not in user_reply_rules:
            user_reply_rules[user] = []  # 初始化为空列表

    if request.method == 'POST':
        selected_user = request.form.get('selected_user')
        keyword = request.form.get('keyword')

        if selected_user and keyword:
            user_reply_rules[selected_user].append({'keyword': keyword, 'response': "抱歉，我无法理解您的请求。"})  # 使用默认响应
            flash('回复规则已添加', 'success')
        else:
            flash('请填写所有字段', 'error')

    return render_template('reply_settings.html', users=user_reply_rules.keys(), user_reply_rules=user_reply_rules)

@app.route('/reply/<input_text>')
def get_reply(input_text):
    reply = robot_message(input_text)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
