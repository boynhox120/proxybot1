import json
import os
from datetime import datetime, timedelta
from threading import Thread

from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === Flask web server để UptimeRobot ping ===
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot vẫn đang chạy nha!'

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# === Telegram bot setup ===
DATA_FILE = "proxy_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nhập proxy gửi đây ní ơi ní")

async def handle_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    data = load_data()
    now_vn = datetime.utcnow() + timedelta(hours=7)
    time_str = now_vn.strftime("%H:%M:%S %d-%m-%Y")

    replies = []
    proxies = [line.strip() for line in user_input.splitlines() if line.strip()]

    for proxy in proxies:
        if proxy in data:
            replies.append(f"NÍ ƠI PROXY {proxy} ĐÃ ĐƯỢC BÀO LÚC {data[proxy]}")
        else:
            data[proxy] = time_str
            replies.append(f"Proxy {proxy} đã được lưu vào {time_str}")

    save_data(data)
    await update.message.reply_text("\n".join(replies))

# === MAIN ===
TOKEN = "7221833132:AAGKcnF9vwmpo-0LftQMW-k1w2EtCfY2sVo"  # Thay bằng token thật

def main():
    Thread(target=run_flask).start()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_proxy))
    print("Bot Telegram đã chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
