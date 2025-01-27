from flask import Flask, render_template, jsonify, request, flash
from core.database import DatabaseManager

app = Flask(__name__)
app.secret_key = 'secret_key'

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
    bots = [ (bot['name'],bot['prompts']) for bot in db.list_bots()]
    for name,prompts in bots:
        if prompts:
            user_reply_rules[name] = prompts
        else:
            user_reply_rules[name] = None

    if request.method == 'POST':
        selected_bot = request.form.get('selected_bot')
        keyword = request.form.get('keyword')

        if selected_bot and keyword:
            user_reply_rules[selected_bot] = keyword
            db.update_bot(selected_bot, keyword)
            flash('回复规则已添加', 'success')
        else:
            user_reply_rules[selected_bot] = None
            db.update_bot(selected_bot, None)
            flash('回复规则已删除', 'success')

    return render_template('reply_settings.html', bots=user_reply_rules.keys(), user_reply_rules=user_reply_rules)


@app.route('/logs')
def logs_page():
    msgs = db.get_logs_order_by_time()
    users_s = [ log['sender'] for log in msgs ]
    users_r = [ log['receiver'] for log in msgs ]
    # combine two lists and remove duplicates
    users = list(set(users_s + users_r))
    logs = [ (msg['time'], msg['msg_type'], msg['sender'], msg['receiver'], msg['content']) for msg in msgs ]
    return render_template('logs.html', users=users, logs=logs[::-1])

# 更新机器人和用户关联的路由
@app.route('/robot-management', methods=['GET', 'POST'])
def robot_management():
    # 机器人列表和用户列表
    robots = [bot['name'] for bot in db.list_bots()]
    users = [{"name":user,"bot":db.get_bot_for_user(user)} for user in load_users_from_file()]

    if request.method == 'POST':
        # 获取机器人和用户的关联信息
        data = request.get_json()
        selected_robot = data.get('robot')
        selected_users = data.get('users')

        # 清除旧的关联
        for user in selected_users:
            db.remove_user_whatever_bot(user)
            db.assign_user_to_bot(selected_robot, user)
            
        return jsonify({'message': '关联已更新'})

    return render_template('robot_management.html', robots=robots, users=users)


@app.route('/create-robot', methods=['POST'])
def create_robot():
    robot_name = request.form.get('robot_name')
    db.save_bot(robot_name, None)
    return '机器人创建请求已收到', 200

@app.route('/delete-robot', methods=['POST'])
def delete_robot():
    robot_name = request.form.get('robot_name')
    db.delete_bot(robot_name)
    return '机器人已删除', 200


if __name__ == '__main__':
    app.run(debug=True)
