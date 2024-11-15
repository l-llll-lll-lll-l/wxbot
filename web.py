from flask import Flask, render_template, jsonify, request, flash, session, send_file
import sqlite3
import csv
from core.database import DatabaseManager

app = Flask(__name__)

db = DatabaseManager('bot.db')

# 用户的回复规则
user_reply_rules = {}
default_reply_rule = {'keyword': '你好', 'response': '你好，有什么我可以帮助你的吗？'}


# 加载用户
def load_users_from_file():
    return db.get_all_users()

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
    msgs = db.get_logs_order_by_time()
    users_s = [ log['sender'] for log in msgs ]
    users_r = [ log['receiver'] for log in msgs ]
    # combine two lists and remove duplicates
    users = list(set(users_s + users_r))
    logs = [ (msg['time'], msg['msg_type'], msg['sender'], msg['receiver'], msg['content']) for msg in msgs ]
    return render_template('logs.html', users=users, logs=logs)

# 更新机器人和用户关联的路由
@app.route('/robot-management', methods=['GET', 'POST'])
def robot_management():
    # 机器人列表和用户列表
    robots = db.list_bots()
    users = load_users_from_file()

    if request.method == 'POST':
        # 获取机器人和用户的关联信息
        data = request.get_json()
        selected_robot = data.get('robot')
        selected_users = data.get('users')

        # 清除旧的关联
        for user in selected_users:
            db.remove_user_whatever_bot(user)
            db.assign_user_to_bot(selected_robot, user)

        return jsonify({'status': 'success'}), 200

    return render_template('robot_management.html', robots=robots, users=users)

if __name__ == '__main__':
    app.run(debug=True)
