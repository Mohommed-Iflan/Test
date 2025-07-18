import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

BOT_TOKEN = "YOUR_BOT_TOKEN"  # replace with actual token

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
async def handle_forwarded_video(message: types.Message):
    # Check if message has a video
    video = message.video
    if not video:
        await message.reply("❌ Please forward a video message (not text or photo).")
        return

    file_id = video.file_id

    try:
        file = await bot.get_file(file_id)
        file_path = file.file_path
        # Optional: hide token in output if needed
        safe_token = "BOT_TOKEN"
        download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        await message.reply(
            f"🎬 <b>File ID:</b>\n<code>{file_id}</code>\n\n"
            f"📥 <b>Download Link:</b>\n<code>{download_link}</code>",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await message.reply(f"❌ Error:\n<code>{str(e)}</code>", parse_mode=ParseMode.HTML)

# Main entry
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())