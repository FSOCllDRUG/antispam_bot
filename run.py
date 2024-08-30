import asyncio
import logging
from decouple import config
from aiogram import Bot, Dispatcher

from handlers.group import group_router


bot = Bot(token=config('API_TOKEN'))
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(group_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
