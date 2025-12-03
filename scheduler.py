# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from database import get_events
from config import ADMIN_CHAT_ID
import asyncio

scheduler = AsyncIOScheduler()

def start_scheduler(bot):
    async def daily_reminder():
        events = get_events()
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        for event in events:
            event_id, title, date_str = event
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if event_date == tomorrow:
                await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Напоминание: {title} завтра ({date_str})")

    async def weekly_reminder():
        events = get_events()
        message = "События на неделю:\n"
        for event in events:
            event_id, title, date_str = event
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if datetime.now().date() <= event_date <= datetime.now().date() + timedelta(days=7):
                message += f"{date_str} - {title}\n"
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

    scheduler.add_job(lambda: asyncio.create_task(daily_reminder()), 'cron', hour=9, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(weekly_reminder()), 'cron', day_of_week='mon', hour=9, minute=0)
    scheduler.start()
