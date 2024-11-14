from wxauto import WeChat
import time
from models import AIModel
import time
import signal
from database import DatabaseManager

class AutoReplyBot:
    def __init__(self, model_path, db_path):
        self.wx = WeChat()
        self.listen_list = []  # 监听列表
        self.model = AIModel(model_path)
        self.db_manager = DatabaseManager(db_path)
        self.running = True  # 添加一个运行标志
        
    def reply(self, message):
        all_content = []
        for content in self.model.chat(message):
            all_content.append(content)
        # concatenate all the content
        return ''.join(all_content)
            

    def add_listen_chat(self, chat_list):
        """添加监听的群组或用户"""
        for chat_name in chat_list:
            self.wx.AddListenChat(who=chat_name)
            print(f"Add {chat_name} to listen list.")

    def auto_reply(self):
        """自动回复消息"""
        wait = 1  # 每隔1秒检查一次是否有新消息
        while self.running:
            msgs = self.wx.GetListenMessage()
            for chat in msgs:
                who = chat.who  # 获取聊天窗口名（人或群名）
                one_msgs = msgs[chat]  # 获取消息内容
                for msg in one_msgs:
                    msgtype = msg.type  # 获取消息类型
                    content = msg.content  # 获取消息内容
                    print(f'【{who}】：{content}')
                    self.db_manager.save_message(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
                                                sender=who, 
                                                receiver='bot', 
                                                content=content, 
                                                msg_type=msgtype)
                    if msgtype == 'friend':  # 如果是好友发来的消息，则回复
                        reply_content = self.reply(content)
                        chat.SendMsg(reply_content)
                        self.db_manager.save_message(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
                                                    sender='bot', 
                                                    receiver=who, 
                                                    content=reply_content, 
                                                    msg_type='reply')
            time.sleep(wait)
                    
    def signal_handler(self, sig, frame):
        # closs the bot
        self.running = False
        self.model.terminate()
        print("Bot is closed.")
        
if __name__ == "__main__":
    bot = AutoReplyBot(model_path="./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC", db_path="bot.db")
    print("Bot is setting listener... it may take a few mins.(wait until all the mumbers below are loaded)")
    
    db = DatabaseManager("bot.db")
    
    bot.add_listen_chat(db.get_users_for_bot("bot4"))

    # 设置信号处理程序
    signal.signal(signal.SIGINT, bot.signal_handler)

    print("Bot is running...")
    bot.auto_reply()