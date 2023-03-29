from pyrogram import filters

from Karma import Karma


@Karma.on_message(filters.command("start"))
async def first(_, message):
    await message.reply_text("Check help in inbox. :)")
