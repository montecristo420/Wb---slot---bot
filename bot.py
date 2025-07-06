
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from checker import check_slots_and_book
from config import TELEGRAM_TOKEN

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот запущен. Проверка слотов будет происходить каждые 30 минут.")

async def manual_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = check_slots_and_book()
    await update.message.reply_text(result)

async def auto_checker(app):
    while True:
        result = check_slots_and_book()
        logging.info(f"[АВТО-ПРОВЕРКА] {result}")
        await asyncio.sleep(1800)

def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", manual_check))

    async def run():
        asyncio.create_task(auto_checker(app))
        await app.run_polling()

    asyncio.run(run())
