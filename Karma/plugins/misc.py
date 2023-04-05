# Copied from old work.
# https://github.com/rozari0/NeedMusicRobot/blob/master/mbot/plugins/greetings.py
from os import execvp, sys

from pyrogram import enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Karma import Karma, PREFIXS
from Karma.utils.filters import is_sudo


@Karma.on_message(filters.command("start", prefixes=PREFIXS))
async def start(_, message):
    await message.reply_text("Bleh!")


helps = {
    "Reward": "Only Sudoers can Reward Member.\nUse **/reward @username 50**(Any Int Value).",
    "Restart": "Only Sudoers can Restart bot.\nUse **/restart** in private.",
    "Rules": "Send ++1 or --1 to give or take karma. (Do not abuse, You'll be blacklisted)",
    "Donation": "Use **/give 25(int)** in reply for donate karma.",
    "Admin": "Use **/blacklist** if you want to blacklist someone and **/rmblacklist** if you want to remove someone from blacklist.\nUse **addsudo** to add someone as Sudo or **rmsudo** to remove someone from Sudo.",
    "Stats": "Use **/stats** for Overall Stats.\nUse **/karmacount** if you want to get karma of specific someone.\nUse **/backup** in private to get DB backup.",
}


@Karma.on_message(filters.command("help", prefixes=PREFIXS))
async def help(_, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply("Send help command in PM. -_-")
    button = [[InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in helps]

    await message.reply_text(
        f"Hello **{message.from_user.mention}**, I'm **Penguins Karma Bot**.",
        reply_markup=InlineKeyboardMarkup(button),
    )


@Karma.on_callback_query(filters.regex(r"help_(.*?)"))
async def helpbtn(_, query):
    i = query.data.replace("help_", "")
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Back", callback_data="helphome")]]
    )
    text = f"Help for **{i}**\n\n{helps[i]}"
    await query.message.edit(text=text, reply_markup=button)


@Karma.on_callback_query(filters.regex(r"helphome"))
async def help_home(_, query):
    button = [[InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in helps]
    await query.message.edit(
        f"Hello **{query.from_user.mention}**, I'm **Penguins Karma Bot**.",
        reply_markup=InlineKeyboardMarkup(button),
    )


@Karma.on_message(
    filters.command("restart", prefixes=PREFIXS) & is_sudo & filters.private
)
async def restart(_, message):
    await message.delete()
    execvp(sys.executable, [sys.executable, "-m", "Karma"])


@Karma.on_message(filters.command("backup") & is_sudo & filters.private)
async def backup(_, message: Message):
    return await message.reply_document("PenguinsKarma.db")
