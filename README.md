# 🌟 Project ShiraCo

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram API](https://img.shields.io/badge/Telegram-Bot%20API-0088cc.svg?logo=telegram)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Repository](https://img.shields.io/badge/GitHub-Project%20ShiraCo-black?logo=github)](https://github.com/ayanoharuka/Project-ShiraCo)

> 一个优雅、轻量级的 Telegram 私信转发机器人，集成了账号信息查询与二次元图库检索功能。

Project ShiraCo 旨在为 Telegram 用户提供一个简单的**双向通讯桥梁**（类似于树洞或客服机器人），同时内置了实用的 TG 账号查询工具和基于 Lolicon API 的插画获取功能。

---

## ✨ 核心功能 (Features)

* 💌 **双向私信转发**：普通用户发送给机器人的消息会直接转发给管理员。管理员只需“回复 (Reply)”该消息，即可将内容传达给对应用户。
* 🔍 **账号信息探针**：
    * 一键获取用户的精确 Telegram ID。
    * 通过解析头像数据，精准查询用户所在的 Telegram 数据中心 (DC ID)。
* 🎨 **插画获取 (Setu)**：接入第三方优质 API，支持自定义 Tag 检索以及混合模式分级查询，一键直达 Pixiv 原链接。
* ⌨️ **现代化交互**：全面采用 InlineKeyboardMarkup (内联键盘) 与用户交互，界面干净整洁。

---

## 🛠️ 部署指南 (Deployment)

### 1. 环境准备
确保您的服务器或本地环境已安装 **Python 3.8 或更高版本**。

### 2. 克隆项目
```bash
git clone [https://github.com/ayanoharuka/Project-ShiraCo.git](https://github.com/ayanoharuka/Project-ShiraCo.git)
cd Project-ShiraCo
```

### 3. 安装依赖
本项目依赖 `python-telegram-bot`, `requests`, `python-dotenv` 以及 `tg-file-id` 等库。
```bash
pip install -r requirements.txt
```

### 4. 配置文件
在项目根目录下创建一个 `.env` 文件，并填入您的 Bot Token 和管理员 ID：
```env
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ
ADMIN_ID=你的Telegram_UID
```
*(注：`ADMIN_ID` 是用于接收私信和拥有回复权限的用户 ID，可通过向机器人发送 `/id` 获取)*

### 5. 运行机器人
```bash
python bot.py
```
当终端输出 `发现 BOT_TOKEN 环境变量并成功应用！` 和 `PM 机器人启动中...` 时，说明机器人已成功上线！

---

## 📚 指令列表 (Commands)

| 指令 | 说明 | 示例 / 备注 |
| :--- | :--- | :--- |
| `/start` | 唤醒并开始使用机器人 | - |
| `/help` | 调出帮助菜单与功能列表 | 包含联系主人的快捷按钮 |
| `/id` | 查询当前账号的 Telegram ID | - |
| `/dc` | 查询当前账号所在的 DC (数据中心) 区域 | *注：需用户设置了公开头像* |
| `/setu` | 随机获取一张二次元插画 | `/setu 猫耳` 或 `/setu 白丝 r18` |

---

## 💡 使用提示
**关于消息回复（仅限管理员）：**
当机器人将用户的私信转发给您时，消息中会包含用户的 ID 和基本信息。如果您想回复该用户，**必须**在 Telegram 中选中那条消息并点击 **“回复 (Reply)”**，然后输入内容发送。机器人会自动解析并把您的话送达给目标用户。

---

## 📄 开源协议 (License)
本项目遵循 [MIT License](https://opensource.org/licenses/MIT) 开源协议。