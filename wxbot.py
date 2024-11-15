import dashboard
import threading
from core.wxutils import AutoReplyBot
import signal
import os
import sys
os.environ['MLC_LLM_HOME'] = "./"


def run_web():
    dashboard.app.run()

def run_bot():
    bot = AutoReplyBot(model_path="./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC", db_path="bot.db")
    print("Bot is running...")
    bot.auto_reply()

def signal_handler(sig, frame):
    sys.exit(0)
    
threading.Thread(target=run_web).start()
run_bot()
signal.signal(signal.SIGINT, signal_handler)
