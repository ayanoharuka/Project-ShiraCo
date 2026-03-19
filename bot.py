import os
from dotenv import load_dotenv
import logging
import requests
import re
from tg_file_id import file_id
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeAllGroupChats, BotCommandScopeDefault
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode, ChatType

# 加载 .env 文件（本地测试用）
load_dotenv()

# 1. 基本设置
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))   # 管理员 ID

# 检查 Token 是否存在
if not TOKEN:
    print("错误：未找到 BOT_TOKEN 环境变量！")
    exit(1)
else:
    print("发现 BOT_TOKEN 环境变量并成功应用！")

# 开启日志，方便调试
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 当用户发送 /start 时
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    full_name = user.full_name
    await update.message.reply_text(f"可以通过我联系 {full_name} ~")

# 当用户发送 /help 时
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    #帮助文本部分
    help_text = (
        "功能列表\n"
        "点击即可使用\n"
        "🔹 基础功能\n"
        "┣ 向主人转发消息（直接发送你需要被转发的消息）\n"
        "┗ /help 显示此帮助信息\n\n"
        "🔹 账号查询\n"
        "┣ /id 查询账号 TGID\n"
        "┗ /dc 查询账号 DC 区域\n"
        "🔹 特殊功能\n"
        "┗ /setu 一键色图\n"
        "   ┗注意: 您可以指定tag和是否为r18\n"
        "    例如 /setu 猫耳 r18\n"
    )

    #帮助文本下放的InlineKeyboardButton（内联按钮）
    help_keyboard = [
        [InlineKeyboardButton("联系主人", url=f"tg://user?id={ADMIN_ID}")],
        [InlineKeyboardButton("关闭菜单", callback_data="close")]
    ]

    reply_markup = InlineKeyboardMarkup(help_keyboard)
    
    #发送部分
    await update.message.reply_text(
        text=help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"你的用户ID为: {user.id}")

async def dc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photos = await user.get_profile_photos()
    
    if photos.total_count > 0:
        latest_photo_file_id = photos.photos[0][-1].file_id
        
        decoded = file_id.from_file_id(latest_photo_file_id)
        dc_id = decoded.dc_id
    
        await update.message.reply_text(f"您的头像存储在：{dc_id}") 
    else:
        await update.message.reply_text("你没有设置头像, 无法查询ID。") 

# 涩图转发
SETU_API_URL = "https://api.lolicon.app/setu/v2"

async def get_setu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 自定请求参数
    r18_status = 0
    custom_tags = []

    if context.args:
        for arg in context.args:
            if arg.lower() == "r18":
                r18_status = 1
            elif arg.lower() == "h": # 混合模式快捷键
                r18_status = 2
            else:
                custom_tags.append(arg) # 其他也当作tag

    # 构建请求参数
    params = {
        "r18": r18_status,
        "num": 1,
        "size": "original",
        "tag": custom_tags
    }

    try:
        # 发送GET请求
        response = requests.get(SETU_API_URL, params=params)
        data = response.json()

        if data.get("data") and len(data["data"]) > 0: 
            item = data["data"][0] 

            # 提取图片网址
            item = data["data"][0]
            img_url = item["urls"]["original"]
            title = item["title"]
            author = item["author"]
            pid = item["pid"]

            # 一键跳转pixiv (inlinekeyboard)
            pixiv_url = f"https://www.pixiv.net/artworks/{pid}"
            keyboard = [[InlineKeyboardButton("在 Pixiv 打开", url=pixiv_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            r18_text = "R18" if r18_status == 1 else "非R18" if r18_status == 0 else "混合模式"
            tags_list = item.get("tags", []) 
            tag_str = "#" + " #".join(tags_list) if tags_list else "无标签"

            # 发送
            await update.message.reply_photo(
                photo=img_url,
                caption=(
                    f"<b>标题: {title}</b>\n"
                    f"作者: {author}\n"
                    f"分级: {r18_text}\n"
                    f"PID: <code>{pid}</code>\n"
                    f"TAG: {tag_str}"
                ),
                reply_markup=reply_markup, 
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text("没找到图呜呜呜")

    except Exception as e:
        await update.message.reply_text(f"出错了: {e}")

# 报错处理
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await print(f"在处理 {Update} 时发现 {context.error} 发生")

# 处理消息转发逻辑
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    chat_id = update.effective_chat.id
    text = update.message.text
    username = f"@{user.username}" if user.username else "无用户名"
    premium_status = "Premium 会员" if user.is_premium else "普通用户"
    lang = user.language_code if user.language_code else "未知"

    if update.effective_chat.type != ChatType.PRIVATE:
        return 

    # 状况 A：普通用户发消息给机器人 -> 转发给管理员
    if chat_id != ADMIN_ID:
        # 转发消息给管理员，并标注用户 ID (格式固定，方便后续正则表达式解析)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"**新私信**\n"
                f"**来自**: [{user.full_name}](tg://user?id={user.id})\n"
                f"**ID**: `{user.id}`\n"
                f"**用户名**: {username}\n"
                f"**语言**: {lang}\n"
                f"**身份**: {premium_status}\n\n"
                f"**内容**: \n{text}"
            ),
            parse_mode='Markdown'
        )
        await update.message.reply_text("[提示] 信息已传送成功")


    else:
        if update.message.reply_to_message:
            try:
                orig_text = update.message.reply_to_message.text
                match = re.search(r"ID: (\d+)", orig_text)
                
                if match:
                    target_user_id = int(match.group(1))
                    # 将管理员的话发送给该用户
                    await context.bot.send_message(
                        chat_id=target_user_id,
                        text=f"回复：\n{text}"
                    )
                    await update.message.reply_text("[提示] 信息已回复成功~")
                else:
                    await update.message.reply_text("[提示] 无法解析用户 ID, 请确保你回复的是那条包含 ID 的转发消息~")
            except Exception as e:
                await update.message.reply_text(f"[提示] 发送失败：{e}")
        else:
            await update.message.reply_text("[提示] 若要回复用户，请直接“回复 (Reply)”该条转发消息~")

async def post_init(application):

    commands = [
        BotCommand("start", "开始使用"),
        BotCommand("help", "帮助信息"),
        BotCommand("id", "查询我的 ID"),
        BotCommand("dc", "查询账号 DC 区域"),
        BotCommand("setu", "随机色图"),
    ]

    await application.bot.set_my_commands(commands, scope=BotCommandScopeDefault())

    await application.bot.set_my_commands(commands, scope=BotCommandScopeAllGroupChats())


if __name__ == '__main__':
    # 创建 Application
    app = ApplicationBuilder().token(TOKEN).build()

    # 注册处理程序
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("dc", dc_command))
    app.add_handler(CommandHandler("setu", get_setu))
    # 监听所有非指令的文字消息
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("PM 机器人启动中...")
    app.run_polling()
