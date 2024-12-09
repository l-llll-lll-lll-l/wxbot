# WXBot - 微信机器人开源项目


## 项目概述
微信机器人项目旨在为没有公司验证的微信个人账户提供宣传营销等业务的半自动化回复解决方案。该项目将利用开源技术、框架和项目，以桌面程序的形式交付，以满足用户在微信平台上进行自动化客户服务和营销的需求。

## 功能特点
- **自动回复**：支持微信消息的自动回复功能。
- **自定义行为**：允许开发者自定义机器人的行为逻辑。
- **管理界面**：通过Flask框架提供简洁的管理界面。
- **多用户支持**：支持关联多个用户账号。

## 环境要求
- Python环境
- Git
- Windows Powershell（仅限Windows用户）

## 安装步骤

### 步骤 1: 获取WXBot仓库
在GitHub上搜索`wxbot`仓库(https://github.com/l-llll-lll-lll-l/wxbot)，并下载压缩包。
<img alt="图片1.png" src="(https://github.com/l-llll-lll-lll-l/wxbot/main/图片1.png)"/>

### 步骤 2: 下载Ollama模型
访问[Ollama官方下载页面](https://ollama.com/download)下载Ollama模型。
<img alt="图片2.png" src="C:\Users\lenovo\Desktop\wechatAI\图片2.png"/>

### 步骤 3: 安装Ollama模型
打开Windows Powershell，输入以下命令安装模型：
ollama run qwen2.5:0.5b
<img alt="图片3.png" src="C:\Users\lenovo\Desktop\wechatAI\图片3.png"/>
<img alt="图片4.png" src="C:\Users\lenovo\Desktop\wechatAI\图片4.png"/>

### 步骤 4: 安装依赖
找到下载的wxbot文件夹，打开终端或命令提示符，输入以下命令安装依赖：
pip install wxauto, flask
<img alt="图片6.png" src="C:\Users\lenovo\Desktop\wechatAI\图片6.png"/>

### 步骤 5: 运行WXBot
在`wxbot`文件夹中，打开终端或命令提示符，输入以下命令启动WXBot：
python wxbot.py
<img alt="图片7.png" src="C:\Users\lenovo\Desktop\wechatAI\图片7.png"/>

### 步骤 6: 访问管理界面
在Powershell中按住`Ctrl`键并点击域名`127.0.0.1:5000`，打开管理界面。

<img alt="图片8.png" src="C:\Users\lenovo\Desktop\wechatAI\图片8.png"/>

### 步骤 7: 创建微信机器人
- 点击“微信机器人管理”。
<img alt="图片9.png" src="C:\Users\lenovo\Desktop\wechatAI\图片9.png"/>
- 点击“创建机器人”，并输入微信机器人名称。
<img alt="图片10.png" src="C:\Users\lenovo\Desktop\wechatAI\图片10.png"/>
- 选择你想关联的用户。
<img alt="图片11.png" src="C:\Users\lenovo\Desktop\wechatAI\图片11.png"/>

### 步骤 8: 正式运行
完成上述步骤后，您的微信机器人即可正式运行。
<img alt="图片12.png" src="C:\Users\lenovo\Desktop\wechatAI\图片12.png"/>

## 贡献指南
我们欢迎任何形式的贡献，包括但不限于代码提交、文档改进、问题报告等。请遵循我们的贡献指南。

## 许可证
本项目采用 [Apache License 2.0](LICENSE)。

## 联系方式
如有任何问题或建议，请通过[GitHub Issues](https://github.com/l-llll-lll-lll-l/wxbot/issues)与我们联系。
