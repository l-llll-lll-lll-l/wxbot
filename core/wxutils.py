from wxauto import WeChat
import time
from models import AIModel

class AutoReplyBot:
    def __init__(self, model_path):
        self.wx = WeChat()
        self.listen_list = []  # 监听列表
        self.model = AIModel(model_path)
        
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

    def auto_reply(self):
        """自动回复消息"""
        wait = 1  # 每隔1秒检查一次是否有新消息
        while True:
            msgs = self.wx.GetListenMessage()
            for chat in msgs:
                who = chat.who  # 获取聊天窗口名（人或群名）
                one_msgs = msgs[chat]  # 获取消息内容
                for msg in one_msgs:
                    msgtype = msg.type  # 获取消息类型
                    content = msg.content  # 获取消息内容
                    print(f'【{who}】：{content}')
                    if msgtype == 'friend':  # 如果是好友发来的消息，则回复
                        chat.SendMsg(self.reply(content))

            time.sleep(wait)

if __name__ == "__main__":
    bot = AutoReplyBot(model_path="./qwen2.5_0.5b/Qwen2.5-0.5B-Instruct-q0f16-MLC")
    # 设置需要监听的群组或用户列表
    listen_list = [
        '罗...',
        "测试"
    ]
    bot.add_listen_chat(listen_list)
    bot.auto_reply()