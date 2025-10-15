from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

helps = {
    "Reward": "Only Sudoers can Reward Member.\nUse **/reward @username 50**(Any Int Value).",
    "Restart": "Only Sudoers can Restart bot.\nUse **/restart** in private.",
    "Rules": "Send ++1 or --1 to give or take karma. (Do not abuse, You'll be blacklisted)",
    "Donation": "Use **/give 25(int)** in reply for donate karma.",
    "Admin": "Use **/blacklist** if you want to blacklist someone and **/rmblacklist** if you want to remove someone from blacklist.\nUse **addsudo** to add someone as Sudo or **rmsudo** to remove someone from Sudo.",
    "Stats": "Use **/stats** for Overall Stats.\nUse **/karmacount** if you want to get karma of specific someone.\nUse **/backup** in private to get DB backup.",
}

# sort helps by key
helps = dict(sorted(helps.items()))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_markdown(
        "Bleh!",
    )


async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /backup is issued."""
    await update.message.reply_document(
        "PenguinsKarma.db",
        caption=f"Here is your backup! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    keyboard = [
        InlineKeyboardButton(text=i, callback_data=f"help_{i}") for i in helps
    ]
    keyboard = [keyboard[i:i + 3] for i in range(0, len(keyboard), 3)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_markdown(
        f"Hello **{user.mention_markdown()}**, I'm **Penguins Karma Bot**.",
        reply_markup=reply_markup,
    )

