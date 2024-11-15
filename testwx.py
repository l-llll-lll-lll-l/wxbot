from wxauto import WeChat

# 创建微信对象
wx = WeChat()

# 获取会话列表
sessions = wx.GetSessionList()

# 遍历会话列表，打印每个会话的名称和最后一条消息内容
for session in sessions:
    print(f"会话名称: {session}")