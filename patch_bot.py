from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import dp, load_events, save_events, OUTPUT_EVENTS_ID, OUTPUT_NOTES_ID

# --- Добавляем кнопки для удаления мероприятия ---
@dp.message_handler(commands=["list"])
async def list_events_with_buttons(message: types.Message):
    events = load_events()
    for i, event in enumerate(events):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Удалить", callback_data=f"delete_event:{i}"))
        kb.add(InlineKeyboardButton("Редактировать", callback_data=f"edit_event:{i}"))
        await message.answer(
            f"{i+1}. {event['title']} | {event['date']} {event['time']} | {event['people']} чел",
            reply_markup=kb
        )

# --- Обработчик кнопок ---
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("delete_event:"))
async def delete_event_callback(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split(":")[1])
    events = load_events()
    if 0 <= index < len(events):
        removed = events.pop(index)
        save_events(events)
        await callback_query.message.edit_text(f"Мероприятие '{removed['title']}' удалено!")
    await callback_query.answer()
