from wxauto import WeChat
wx = WeChat()
# 给文件传输助手发送消息
wx.SendMsg('这是通过wxauto发给你的消息！', '文件传输助手')