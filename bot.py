import os
import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is not set in environment variables!")

# Initialize bot and dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Match format: filename.mp4 https://t.me/...
LINK_REGEX = re.compile(r"^(?P<filename>.+\.mp4)\s+(?P<link>https://t\.me/[^\s]+)$")


@dp.message()
async def handle_message(message: Message):
    match = LINK_REGEX.match(message.text.strip())
    if not match:
        await message.answer("❌ Send in this format:\n<code>filename.mp4 https://t.me/...</code>")
        return

    filename = match.group("filename")
    link = match.group("link")

    try:
        # Try to get the message from the link
        extracted = await bot.get_chat_message_by_url(link)
        if extracted.video:
            file_id = extracted.video.file_id
            await message.answer(f"✅ File ID:\n<code>{file_id}</code>")
        else:
            await message.answer("❌ No video found in that message.")
    except Exception as e:
        await message.answer(f"❌ Failed to fetch video from link:\n<code>{e}</code>")


async def main():
    print("🚀 Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())