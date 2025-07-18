import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from aiogram.client.session.aiohttp import AiohttpSession

BOT_TOKEN = "YOUR_BOT_TOKEN"

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create bot instance with default HTML parse mode
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)

# Dispatcher
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    # Check if message is a forwarded video
    if message.video or message.forward_from or message.forward_from_chat:
        video = message.video

        if not video:
            await message.reply("❌ No video found in the forwarded message.")
            return

        file_id = video.file_id

        # Get file path
        try:
            file = await bot.get_file(file_id)
            file_path = file.file_path
            download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

            response_text = (
                f"🎬 <b>Video file_id</b>:\n<code>{file_id}</code>\n\n"
                f"📥 <b>Download link</b>:\n<code>{download_link}</code>"
            )
            await message.reply(response_text)
        except Exception as e:
            await message.reply(f"❌ Failed to get file path:\n<code>{e}</code>")
    else:
        await message.reply("❌ Please forward a video to get the file ID and path.")

# Main
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())