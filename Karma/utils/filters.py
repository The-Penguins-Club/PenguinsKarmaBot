from pyrogram import filters
from pyrogram.types import Message

from Karma import SUDOERS
from Karma.utils.dbhelpers import get_user


async def is_sudo(_, __, message: Message):
    if not message.from_user:
        return False
    if get_user(message.from_user.id).is_sudo:
        return True
    if message.from_user.id in SUDOERS:
        return True
    await message.reply("This Feature is Only For Sudo Users.")
    return False


is_sudo = filters.create(is_sudo)


async def is_whitelisted(_, __, message: Message):
    if not message.from_user:
        await message.reply("You Or the user you are replying is Anon.")
        return False
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            False

    user = get_user(message.from_user.id)
    return not user.is_blacklisted


is_whitelisted = filters.create(is_whitelisted)
