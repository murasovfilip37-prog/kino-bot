import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = "8723320552:AAHwX7FjjnksbxmzTe6ZlMs6SRtwd36KnPI"

# Укажите ваш настоящий канал (юзернейм и ссылку)
CHANNEL_USERNAME = "@KinoPoiskBt"  # Например: "@kinoclub"
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
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
    return False

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)
    
    if not is_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="🔄 Я подписался", callback_data="check_sub")]
        ])
        await message.answer(
            "Привет! 🎬 Чтобы пользоваться ботом, пожалуйста, подпишитесь на наш канал:",
            reply_markup=keyboard
        )
        return

    await message.answer("Приветствую! 🎬 Отправьте мне цифровой код фильма, и я скажу его название!")

# ОБРАБОТЧИК КНОПКИ «Я подписался»
@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: CallbackQuery):
    user_id = callback.from_user.id
    is_subscribed = await check_subscription(user_id)
    
    if is_subscribed:
        # Убираем кнопку и пишем об успешной проверке
        await callback.message.edit_text("Спасибо за подписку! 🎉 Теперь отправьте мне цифровой код фильма:")
    else:
        # Если все еще не подписан, показываем уведомление во всплывающем окне
        await callback.answer("Вы еще не подписались на канал! ❌ Подпишитесь, а затем нажмите кнопку снова.", show_alert=True)

# Обработка текстовых кодов
@dp.message(F.text)
async def check_movie_code(message: Message):
    user_id = message.from_user.id
    
    is_subscribed = await check_subscription(user_id)
    if not is_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="🔄 Я подписался", callback_data="check_sub")]
        ])
        await message.answer("⚠️ Сначала подпишитесь на канал, чтобы отправлять коды!", reply_markup=keyboard)
        return

    code = message.text.strip()
    
    if code in MOVIES_DB:
        movie_name = MOVIES_DB[code]
        await message.answer(f"Нашел для вас фильм: <b>{movie_name}</b> 🍿")
    else:
        await message.answer("Упс! Фильм с таким кодом не найден в базе. Проверьте правильность кода.")

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.add_routes([web.get("/", handle)])

async def web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
