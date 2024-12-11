import dashboard
import threading
from core.wxutils import AutoReplyBot
import signal
from const import modelname, db_path

def run_web():
    dashboard.app.run()

def run_bot():
    bot = AutoReplyBot(modelname=modelname, db_path=db_path)
    signal.signal(signal.SIGINT, bot.signal_handler)
    print("Bot is running...(use Ctrl+C to stop the bot)")
    bot.auto_reply()

print("Starting bot and web dashboard...")
threading.Thread(target=run_web).start()
run_bot()
print("close the window to exit")