import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import json
import os

# -------------------------------------
# НАСТРОЙКИ
# -------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render environment variable
INPUT_GROUP_ID = -5012773570
OUTPUT_GROUP_ID = -1003264984732

DATA_FILE = "events.json"

logging.basicConfig(level=logging.INFO)

# -------------------------------------
# ФУНКЦИИ РАБОТЫ С ДАННЫМИ
# -------------------------------------
def load_events():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_events(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def weekday_name(date_str):
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return days[dt.weekday()]

# -------------------------------------
# ЛОГИКА БОТА
# -------------------------------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -------------------------------------
# Команда для просмотра всех мероприятий
# -------------------------------------
@dp.message(Command("list"))
async def list_events(message: types.Message):
    events = load_events()

    if not events:
        await message.answer("Пока нет ни одного мероприятия.")
        return

    text = "📅 *Список мероприятий:*\n\n"
    for i, e in enumerate(events, start=1):
        text += (
            f"*{i}. {e['title']}*\n"
            f"Дата: {e['date']} ({weekday_name(e['date'])})\n"
            f"Время: {e['time']}\n"
            f"Количество человек: {e['count']}\n\n"
        )

    await message.answer(text, parse_mode="Markdown")

# -------------------------------------
# Приём новых мероприятий из входной группы
# -------------------------------------
@dp.message()
async def add_event(message: types.Message):
    if message.chat.id != INPUT_GROUP_ID:
        return

    text = message.text.strip()

    # Формат:
    # Название | YYYY-MM-DD | HH:MM | Кол-во
    try:
        title, date_str, time_str, count = [x.strip() for x in text.split("|")]

        datetime.strptime(date_str, "%Y-%m-%d")
        datetime.strptime(time_str, "%H:%M")

        event = {
            "title": title,
            "date": date_str,
            "time": time_str,
            "count": int(count)
        }

        events = load_events()
        events.append(event)
        save_events(events)

        await message.reply("Мероприятие добавлено! ✔️")

    except Exception:
        await message.reply(
            "❗ Неверный формат\nИспользуй:\n"
            "`Название | 2025-01-30 | 18:30 | 25`",
            parse_mode="Markdown"
        )

# -------------------------------------
# Удаление мероприятия
# -------------------------------------
@dp.message(Command("delete"))
async def delete_event(message: types.Message):
    try:
        index = int(message.text.split()[1]) - 1
        events = load_events()

        if not 0 <= index < len(events):
            raise ValueError

        removed = events.pop(index)
        save_events(events)

        await message.answer(
            f"Мероприятие *{removed['title']}* удалено.",
            parse_mode="Markdown"
        )

    except:
        await message.answer("Использование: `/delete 1`", parse_mode="Markdown")

# -------------------------------------
# НАПОМИНАНИЕ ЗА ДЕНЬ ДО ДАТЫ
# -------------------------------------
async def daily_notifications():
    events = load_events()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    notify = [e for e in events if e["date"] == tomorrow]

    if notify:
        text = "🔔 *Напоминание о завтрашних мероприятиях:*\n\n"
        for e in notify:
            text += (
                f"• {e['title']}\n"
                f"Время: {e['time']}\n"
                f"Людей: {e['count']}\n\n"
            )
        await bot.send_message(OUTPUT_GROUP_ID, text, parse_mode="Markdown")

# -------------------------------------
# Еженедельный отчёт
# -------------------------------------
async def weekly_report():
    today = datetime.now()
    monday = today + timedelta(days=(7 - today.weekday()))

    events = load_events()

    next_week = []
    for e in events:
        dt = datetime.strptime(e["date"], "%Y-%m-%d")
        if monday <= dt < monday + timedelta(days=7):
            next_week.append(e)

    if not next_week:
        text = "На следующую неделю мероприятий нет."
    else:
        text = "📆 *Мероприятия на следующую неделю:*\n\n"
        for e in next_week:
            text += (
                f"*{e['title']}*\n"
                f"{e['date']} — {weekday_name(e['date'])}\n"
                f"Время: {e['time']}\n"
                f"Людей: {e['count']}\n\n"
            )

    await bot.send_message(OUTPUT_GROUP_ID, text, parse_mode="Markdown")

# -------------------------------------
# Запуск бота
# -------------------------------------
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_notifications, "cron", hour=9, minute=0)
    scheduler.add_job(weekly_report, "cron", day_of_week="mon", hour=9, minute=0)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
