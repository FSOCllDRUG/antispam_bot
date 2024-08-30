import asyncio
import json
from decouple import config
from aiogram import types, Router, F, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from nltk import word_tokenize
from filters.chat_type import ChatTypeFilter


bot = Bot(token=config('API_TOKEN'))

group_router = Router()
# Загрузка словаря из файла
with open('data/word_freq.json', 'r', encoding='utf-8') as f:
    word_freq = json.load(f)

# Пороговые значения
LOW_THRESHOLD = 10
HIGH_THRESHOLD = 30

# Хранилище для подтверждений
confirmation_storage = {}


@group_router.message(F.text, ChatTypeFilter(chat_type=["group", "supergroup"]))
async def filter_spam(message: types.Message):
    message_words = word_tokenize(message.text.lower())
    total_freq = sum(word_freq.get(word, 0) for word in message_words)

    if total_freq > HIGH_THRESHOLD:
        await message.delete()
        await bot.ban_chat_member(message.chat.id, message.from_user.id)
        # Удаление сервисного сообщения
        await asyncio.sleep(1)  # Небольшая задержка, чтобы сообщение успело появиться
        await bot.delete_message(message.chat.id, message.message_id + 1)
    elif total_freq > LOW_THRESHOLD:
        # Создание инлайн-кнопки для подтверждения спама
        button = InlineKeyboardButton(text="Это спам", callback_data=f"confirm_spam_{message.message_id}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
        await message.reply("Сообщение может быть спамом. Подтвердите, пожалуйста.", reply_markup=keyboard)
        confirmation_storage[message.message_id] = []


@group_router.callback_query(lambda c: c.data and c.data.startswith('confirm_spam_'))
async def process_callback(callback_query: CallbackQuery):
    message_id = int(callback_query.data.split('_')[-1])
    user_id = callback_query.from_user.id

    if message_id in confirmation_storage:
        if user_id not in confirmation_storage[message_id]:
            confirmation_storage[message_id].append(user_id)

        if len(confirmation_storage[message_id]) >= 3:
            await bot.delete_message(callback_query.message.chat.id, message_id)
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            await bot.ban_chat_member(callback_query.message.chat.id,
                                      callback_query.message.reply_to_message.from_user.id)
            # Удаление сервисного сообщения
            await asyncio.sleep(1)  # Небольшая задержка, чтобы сообщение успело появиться
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id + 1)

            await callback_query.answer("Сообщение удалено как спам.")
            del confirmation_storage[message_id]
        else:
            button = InlineKeyboardButton(text=f"Это спам ({len(confirmation_storage[message_id])}/3)",
                                          callback_data=f"confirm_spam_{message_id}")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
            await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=keyboard)
            await callback_query.answer(f"Подтверждений: {len(confirmation_storage[message_id])}/3")
    else:
        await callback_query.answer("Сообщение уже удалено или не найдено.")