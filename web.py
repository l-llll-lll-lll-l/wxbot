import subprocess
import threading
import os
from flask import Flask, render_template, request, jsonify
import re

# 初始化Flask应用
app = Flask(__name__)

# 存储聊天日志
global chat_logs
chat_logs = []

# 启动helloworld.py文件的函数
def run_helloworld():
    script_path = os.path.join(os.getcwd(), 'helloworld.py')
    process = subprocess.Popen(
        ['python', script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        encoding='utf-8',  # 指定编码为 utf-8
    )

    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')  # 匹配 ANSI 转义序列

    # 获取实时输出
    for line in iter(process.stdout.readline, ''):
        if line.strip():
            clean_line = ansi_escape.sub('', line.strip())  # 去除 ANSI 转义序列
            print("Output:", clean_line)  # 在控制台打印调试信息，确保子进程有输出
            chat_logs.append(clean_line)

    # 捕获错误输出
    for err_line in iter(process.stderr.readline, ''):
        if err_line.strip():
            clean_err_line = ansi_escape.sub('', err_line.strip())  # 去除 ANSI 转义序列
            print("Error:", clean_err_line)

    process.stdout.close()
    process.stderr.close()
    process.wait()

# 启动一个线程来运行聊天机器人
def start_bot_thread():
    bot_thread = threading.Thread(target=run_helloworld, daemon=True)
    bot_thread.start()

# 首页显示状态
@app.route('/')
def index():
    return render_template('index.html')

# API用来获取当前的聊天记录
@app.route('/get_chat_logs', methods=['GET'])
def get_chat_logs():
    return jsonify({'chat_logs': chat_logs})

# 启动聊天机器人的接口
@app.route('/start_bot', methods=['POST'])
def start_bot():
    start_bot_thread()
    return jsonify({'status': 'bot started'})

if __name__ == "__main__":
    # 设置环境变量
    os.environ['MLC_LLM_HOME'] = "./"
    app.run(host='0.0.0.0', port=5000, debug=True)
