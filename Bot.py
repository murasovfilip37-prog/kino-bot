import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

TOKEN = "8723320552:AAHwX7fjjinksbxmzTe6Z1Ms6SRtwd36KnPI"

# Укажите ваш настоящий канал
CHANNEL_USERNAME = "@KinoPoiskBt" 
CHANNEL_URL = "https://t.me/KinoPoiskBt"

MOVIES_DB = {
    "0001": "Человек-паук",
    "0002": "Интерстеллар",
    "0003": "Титаник",
    "0004": "Матрица",
    "0005": "Аватар"
}

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Функция проверки подписки
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    is_subbed = await check_subscription(message.from_user.id)
    if not is_subbed:
        text = (
            f"❌ Для использования бота необходимо подписаться на наш канал!\n\n"
            f"👉 <a href='{CHANNEL_URL}'>Подписаться на канал</a>\n\n"
            f"После подписки отправьте команду /start снова."
        )
        await message.answer(text, disable_web_page_preview=True)
    else:
        await message.answer("Привет! Отправь мне код фильма (например, 0001), и я вышлю тебе название.")

# Обработчик текстовых сообщений (кодов фильмов)
@dp.message()
async def get_movie(message: Message):
    is_subbed = await check_subscription(message.from_user.id)
    if not is_subbed:
        text = (
            f"❌ Для использования бота необходимо подписаться на наш канал!\n\n"
            f"👉 <a href='{CHANNEL_URL}'>Подписаться на канал</a>"
        )
        await message.answer(text, disable_web_page_preview=True)
        return

    code = message.text.strip()
    if code in MOVIES_DB:
        movie_name = MOVIES_DB[code]
        await message.answer(f"Нашел для вас фильм: <b>{movie_name}</b> 🍿")
    else:
        await message.answer("Упс! Фильм с таким кодом не найден в базе. Проверьте правильность кода.")

# Настройка веб-сервера для Render (чтобы порт был открыт)
async def handle(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.add_routes([web.get("/", handle)])

async def web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

# Главная функция запуска всего вместе
async def main():
    print("Бот успешно запущен!")
    await asyncio.gather(
        web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
