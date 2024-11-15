from wxauto import WeChat
import time
from .models import AIModel
import time
import signal
from .database import DatabaseManager

class AutoReplyBot:
    def __init__(self, model_path, db_path):
        self.wx = WeChat()
        self.listen_list = []  # 监听列表
        self.model = AIModel(model_path)
        self.db_manager = DatabaseManager(db_path)
        self.running = True  # 添加一个运行标志
        print("请等待机器人初始化...（可能需要几分钟）")
        self.db_manager.reset_users_with_list(self.get_all_sessions())
        self.add_listen_chat()
        
    def reply(self, message, chat_name):
        all_content = []
        bot = self.db_manager.get_bot_for_user(chat_name)
        if not bot: # 如果这个机器人在数据库中没有找到，那么就不回复（可能是运行中机器人被删除）
            return None
        prompts = self.db_manager.get_bot(bot)['prompts']
        # 我们先只用一条提示词
        self.model.update_known_info([]) # 先清空
        if prompts:
            self.model.update_known_info([prompts]) 
        for content in self.model.chat(message):
            all_content.append(content)
        return ''.join(all_content)
            
    def add_listen_chat(self):
        """添加监听的群组或用户"""
        chat_list = self.get_all_listen_chat()
        for chat_name in chat_list:
            self.wx.AddListenChat(who=chat_name)
            print(f"Add {chat_name} to listen list.")

    def auto_reply(self):
        """自动回复消息"""
        wait = 1  
        while self.running:
            msgs = self.wx.GetListenMessage()
            for chat in msgs:
                who = chat.who  # 获取聊天窗口名（人或群名）
                one_msgs = msgs[chat]  # 获取消息内容
                for msg in one_msgs:
                    msgtype = msg.type  # 获取消息类型
                    content = msg.content  # 获取消息内容
                    print(f'【{who}】：{content}')
                    self.db_manager.save_log(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
                                                sender=who, 
                                                receiver='bot', 
                                                content=content, 
                                                msg_type=msgtype)
                    if msgtype == 'friend':  # 如果是好友发来的消息，则回复
                        reply_content = self.reply(content, chat.who)
                        if reply_content:
                            chat.SendMsg(reply_content)
                            self.db_manager.save_log(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
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
        
    def get_all_sessions(self):
        list = []
        sessions = self.wx.GetSessionList()
        for session in sessions:
            list.append(session)
        return list
    
    def get_all_listen_chat(self):
        bots = self.db_manager.list_bots()
        users = []
        for bot in bots:
            users.append(self.db_manager.get_users_for_bot(bot['name']))
        rst = []
        for user in users:
            rst.extend(user)
        rst = list(set(rst)) # 正常来说没有重复，但是还是保守的加入去重
        return rst
    
if __name__ == "__main__":
    bot = AutoReplyBot(model_path="./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC", db_path="bot.db")
    # 设置信号处理程序（用于Ctrl+C退出）
    signal.signal(signal.SIGINT, bot.signal_handler)
    print("Bot is running...")
    bot.auto_reply()