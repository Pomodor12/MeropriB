# handlers.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from database import add_event, get_events
from config import INPUT_CHAT_ID

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != INPUT_CHAT_ID:
        return
    try:
        title = context.args[0]
        date = context.args[1]  # формат YYYY-MM-DD
        add_event(title, date)
        await update.message.reply_text(f"Событие '{title}' добавлено на {date}")
    except IndexError:
        await update.message.reply_text("Используй: /add <название> <YYYY-MM-DD>")

async def list_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = get_events()
    if not events:
        await update.message.reply_text("Событий нет")
        return
    message = "Будущие события:\n"
    for event in events:
        event_id, title, date_str = event
        message += f"{date_str} - {title}\n"
    await update.message.reply_text(message)

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        event_id = int(context.args[0])
        delete_event(event_id)
        await update.message.reply_text(f"Событие с ID {event_id} удалено.")
    except (IndexError, ValueError):
        await update.message.reply_text("Используй: /delete <ID_события>")
