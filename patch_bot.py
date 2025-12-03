from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from main import dp, load_events, save_events, load_notes, save_notes, OUTPUT_EVENTS_ID, OUTPUT_NOTES_ID, bot
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# CallbackData для кнопок
event_cb = CallbackData("event", "action", "index")
note_cb = CallbackData("note", "action", "index")

scheduler = AsyncIOScheduler()
scheduler.start()

# ------------------ МЕРОПРИЯТИЯ ------------------

# Список мероприятий с кнопками
@dp.message_handler(commands=["list"])
async def list_events_with_buttons(message: types.Message):
    events = load_events()
    if not events:
        await message.answer("Список мероприятий пуст.")
        return
    for i, event in enumerate(events):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("Удалить", callback_data=event_cb.new(action="delete", index=i)),
            InlineKeyboardButton("Редактировать", callback_data=event_cb.new(action="edit", index=i))
        )
        await message.answer(
            f"{i+1}. {event['title']} | {event['date']} {event['time']} | {event['people']} чел",
            reply_markup=kb
        )

# Кнопки мероприятий
@dp.callback_query_handler(event_cb.filter())
async def event_callback(call: types.CallbackQuery, callback_data: dict):
    index = int(callback_data["index"])
    action = callback_data["action"]
    events = load_events()

    if action == "delete":
        if 0 <= index < len(events):
            removed = events.pop(index)
            save_events(events)
            await call.message.edit_text(f"Мероприятие '{removed['title']}' удалено!")
        await call.answer()

    elif action == "edit":
        # Тут можно добавить отдельный обработчик для редактирования
        await call.answer("Функция редактирования пока не реализована.")

# ------------------ ЗАМЕТКИ ------------------

# Добавление заметки
@dp.message_handler(commands=["note"])
async def add_note(message: types.Message):
    try:
        # Формат: /note Название | YYYY-MM-DD HH:MM
        text = message.text.split(" ", 1)[1]
        title, dt_str = map(str.strip, text.split("|"))
        remind_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        notes = load_notes()
        notes.append({"title": title, "datetime": remind_time.strftime("%Y-%m-%d %H:%M")})
        save_notes(notes)
        await message.answer(f"Заметка '{title}' добавлена и будет напоминать {remind_time}")
        # Планируем напоминание
        scheduler.add_job(
            send_note_reminder,
            "date",
            run_date=remind_time,
            args=[title],
        )
    except Exception as e:
        await message.answer("Ошибка формата. Используйте: /note Название | YYYY-MM-DD HH:MM")

# Список заметок с кнопками
@dp.message_handler(commands=["notes"])
async def list_notes_with_buttons(message: types.Message):
    notes = load_notes()
    if not notes:
        await message.answer("Список заметок пуст.")
        return
    for i, note in enumerate(notes):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("Удалить", callback_data=note_cb.new(action="delete", index=i)),
            InlineKeyboardButton("Редактировать", callback_data=note_cb.new(action="edit", index=i))
        )
        await message.answer(
            f"{i+1}. {note['title']} | {note['datetime']}",
            reply_markup=kb
        )

# Кнопки заметок
@dp.callback_query_handler(note_cb.filter())
async def note_callback(call: types.CallbackQuery, callback_data: dict):
    index = int(callback_data["index"])
    action = callback_data["action"]
    notes = load_notes()

    if action == "delete":
        if 0 <= index < len(notes):
            removed = notes.pop(index)
            save_notes(notes)
            await call.message.edit_text(f"Заметка '{removed['title']}' удалена!")
        await call.answer()

    elif action == "edit":
        await call.answer("Редактирование заметок пока не реализовано.")

# ------------------ НАПОМИНАНИЯ ------------------

async def send_event_reminder(event):
    await bot.send_message(OUTPUT_EVENTS_ID,
        f"Напоминание о мероприятии:\n{event['title']} | {event['date']} {event['time']} | {event['people']} чел"
    )

async def send_note_reminder(title):
    await bot.send_message(OUTPUT_NOTES_ID,
        f"Напоминание о заметке:\n{title}"
    )
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from main import dp, load_events, save_events, load_notes, save_notes, OUTPUT_EVENTS_ID, OUTPUT_NOTES_ID, bot
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# CallbackData для кнопок
event_cb = CallbackData("event", "action", "index")
note_cb = CallbackData("note", "action", "index")

scheduler = AsyncIOScheduler()
scheduler.start()

# ------------------ МЕРОПРИЯТИЯ ------------------

# Список мероприятий с кнопками
@dp.message_handler(commands=["list"])
async def list_events_with_buttons(message: types.Message):
    events = load_events()
    if not events:
        await message.answer("Список мероприятий пуст.")
        return
    for i, event in enumerate(events):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("Удалить", callback_data=event_cb.new(action="delete", index=i)),
            InlineKeyboardButton("Редактировать", callback_data=event_cb.new(action="edit", index=i))
        )
        await message.answer(
            f"{i+1}. {event['title']} | {event['date']} {event['time']} | {event['people']} чел",
            reply_markup=kb
        )

# Кнопки мероприятий
@dp.callback_query_handler(event_cb.filter())
async def event_callback(call: types.CallbackQuery, callback_data: dict):
    index = int(callback_data["index"])
    action = callback_data["action"]
    events = load_events()

    if action == "delete":
        if 0 <= index < len(events):
            removed = events.pop(index)
            save_events(events)
            await call.message.edit_text(f"Мероприятие '{removed['title']}' удалено!")
        await call.answer()

    elif action == "edit":
        # Тут можно добавить отдельный обработчик для редактирования
        await call.answer("Функция редактирования пока не реализована.")

# ------------------ ЗАМЕТКИ ------------------

# Добавление заметки
@dp.message_handler(commands=["note"])
async def add_note(message: types.Message):
    try:
        # Формат: /note Название | YYYY-MM-DD HH:MM
        text = message.text.split(" ", 1)[1]
        title, dt_str = map(str.strip, text.split("|"))
        remind_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        notes = load_notes()
        notes.append({"title": title, "datetime": remind_time.strftime("%Y-%m-%d %H:%M")})
        save_notes(notes)
        await message.answer(f"Заметка '{title}' добавлена и будет напоминать {remind_time}")
        # Планируем напоминание
        scheduler.add_job(
            send_note_reminder,
            "date",
            run_date=remind_time,
            args=[title],
        )
    except Exception as e:
        await message.answer("Ошибка формата. Используйте: /note Название | YYYY-MM-DD HH:MM")

# Список заметок с кнопками
@dp.message_handler(commands=["notes"])
async def list_notes_with_buttons(message: types.Message):
    notes = load_notes()
    if not notes:
        await message.answer("Список заметок пуст.")
        return
    for i, note in enumerate(notes):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("Удалить", callback_data=note_cb.new(action="delete", index=i)),
            InlineKeyboardButton("Редактировать", callback_data=note_cb.new(action="edit", index=i))
        )
        await message.answer(
            f"{i+1}. {note['title']} | {note['datetime']}",
            reply_markup=kb
        )

# Кнопки заметок
@dp.callback_query_handler(note_cb.filter())
async def note_callback(call: types.CallbackQuery, callback_data: dict):
    index = int(callback_data["index"])
    action = callback_data["action"]
    notes = load_notes()

    if action == "delete":
        if 0 <= index < len(notes):
            removed = notes.pop(index)
            save_notes(notes)
            await call.message.edit_text(f"Заметка '{removed['title']}' удалена!")
        await call.answer()

    elif action == "edit":
        await call.answer("Редактирование заметок пока не реализовано.")

# ------------------ НАПОМИНАНИЯ ------------------

async def send_event_reminder(event):
    await bot.send_message(OUTPUT_EVENTS_ID,
        f"Напоминание о мероприятии:\n{event['title']} | {event['date']} {event['time']} | {event['people']} чел"
    )

async def send_note_reminder(title):
    await bot.send_message(OUTPUT_NOTES_ID,
        f"Напоминание о заметке:\n{title}"
    )
