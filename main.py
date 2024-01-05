import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from core.handlers.basic import search_by_address, find_arc, find_bs_info
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold


GOORANDA = "6001130506:AAFNMXUh-iE3zdSq7PK2cpWWg4JFg_swwwg"
JARVIS = "6357305111:AAHzb68csA1ojiDn620m7FFvDXcTP9tYu_s"

CURRENT_BOT = JARVIS



async def start_bot(message:Message,bot: Bot):
    await message.answer(text="Бот запущен!")

async def stop_bot(message: Message,bot: Bot):
    await message.answer(text="Бот остановлен!")

async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=CURRENT_BOT,parse_mode="HTML")

    dp = Dispatcher()
    dp.message.register(find_arc, F.text.upper().startswith("ARC"))
    dp.message.register(search_by_address, F.text.replace(" ","").isalpha())
    dp.message.register(find_bs_info, F.text.replace(" ","").isalnum())



    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())













if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())