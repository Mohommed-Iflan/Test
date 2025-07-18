import os
import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.markdown import hcode
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is not set in environment variables!")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Regex to extract <filename>.mp4 <telegram_link>
LINK_REGEX = re.compile(r"^(.+\.mp4)\s+(https://t\.me/\S+)$")


@dp.message()
async def handle_message(message: Message):
    text = message.text.strip()

    match = LINK_REGEX.match(text)
    if not match:
        await message.reply("❌ Send in this format:\n<code>filename.mp4 https://t.me/...</code>", parse_mode=ParseMode.HTML)
        return

    filename, tg_link = match.groups()

    try:
        # Extract message ID and chat ID
        if "/c/" in tg_link:
            parts = tg_link.split("/")
            chat_id = int("-100" + parts[4])
            msg_id = int(parts[5])
        else:
            # public channel link
            parts = tg_link.split("/")
            chat_username = parts[3]
            msg_id = int(parts[4])
            chat_id = chat_username

        # Fetch message from chat
        msg = await bot.forward_message(chat_id=message.chat.id, from_chat_id=chat_id, message_id=msg_id)

        if not msg.video:
            await message.reply("❌ No video found in the linked message.")
            return

        file_id = msg.video.file_id

        # Get file info
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        await message.reply(
            f"✅ <b>Upload Info</b>\n"
            f"📁 <b>File name:</b> {filename}\n"
            f"🆔 <b>File ID:</b>\n<code>{file_id}</code>\n"
            f"📥 <b>File path:</b>\n<code>{file_path}</code>\n"
            f"🔗 <b>Download link:</b>\n<code>{download_url}</code>",
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        await message.reply(f"❌ Failed to fetch video from link:\n<code>{e}</code>", parse_mode=ParseMode.HTML)


# Health check endpoint for Railway
async def health_check(request):
    return web.Response(text="✅ Bot is working!")


async def main():
    app = web.Application()
    app.router.add_get("/", health_check)

    # Start polling and webhook app together
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())