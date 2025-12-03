# bot.py
import asyncio
from telegram.ext import ApplicationBuilder
from handlers import add, list_events
from scheduler.py import start_scheduler
from config import TOKEN

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_events))

    start_scheduler(app.bot)

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
