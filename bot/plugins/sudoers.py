from telegram import Update
from telegram.ext import ContextTypes

from Karma.utils.dbhelpers import get_user


async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a user to sudoers when the command /addsudo is issued."""
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to a user to add them as sudo.")
    user = update.message.reply_to_message.from_user
    if not user:
        return await update.message.reply_text("Can't add an anonymous user as sudo.")
    _user = get_user(user.id)
    _user.is_sudo = True
    _user.save()
    await update.message.reply_text(
        f"{user.mention_markdown()} has been added as sudo.", parse_mode="Markdown"
    )


async def remove_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a user from sudoers when the command /rmsudo is issued."""
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Reply to a user to remove them from sudo."
        )
    user = update.message.reply_to_message.from_user
    if not user:
        return await update.message.reply_text(
            "Can't remove an anonymous user from sudo."
        )
    _user = get_user(user.id)
    if not _user.is_sudo:
        return await update.message.reply_text(
            f"{user.mention_markdown()} is not a sudo user.", parse_mode="Markdown"
        )
    _user.is_sudo = False
    _user.save()
    await update.message.reply_text(
        f"{user.mention_markdown()} has been removed from sudo.", parse_mode="Markdown"
    )
