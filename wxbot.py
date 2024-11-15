import dashboard
import threading
from core.wxutils import AutoReplyBot
import os
import signal
os.environ['MLC_LLM_HOME'] = "./"


def run_web():
    dashboard.app.run()

def run_bot():
    bot = AutoReplyBot(model_path="./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC", db_path="bot.db")
    signal.signal(signal.SIGINT, bot.signal_handler)
    print("Bot is running...(use Ctrl+C to stop the bot)")
    bot.auto_reply()

print("Starting bot and web dashboard...")
threading.Thread(target=run_web).start()
run_bot()
print("close the window to exit")