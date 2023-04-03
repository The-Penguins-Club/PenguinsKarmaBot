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


async def is_blacklisted(_, __, message: Message):
    if not message.from_user or not message.reply_to_message.from_user:
        await message.reply("You Or the user you are replying is Anon.")
        return True
    if get_user(message.from_user.id).is_blacklisted:
        return True
    return False


is_blacklisted = filters.create(is_blacklisted)
