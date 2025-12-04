import logging
from typing import List

from decouple import config
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, filters

from bot.plugins.misc import backup, help_command, help_home, helpbtn, restart, start
from bot.plugins.sudoers import addsudo, remove_sudo
from Karma.utils.dbhelpers import User

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
BOT_TOKEN = config("BOT_TOKEN")
SUDOERS: List[int] = config("SUDOERS", cast=lambda x: [int(i) for i in x.split()])
NETWORK = config("NETWORK", cast=int)


print(f"Sudoers: {SUDOERS}")
print(f"Network: {NETWORK}, {type(NETWORK)}")


def get_sudoers() -> List[int]:
    for user in User.select().where(User.is_sudo):
        if user.user_id not in SUDOERS:
            SUDOERS.append(user.user_id)
    return SUDOERS


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        CommandHandler(
            "restart", restart, filters=filters.Chat(SUDOERS) & filters.ChatType.PRIVATE
        )
    )
    application.add_handler(
        CommandHandler(
            "backup", backup, filters=filters.Chat(SUDOERS) & filters.ChatType.PRIVATE
        )
    )
    application.add_handler(CallbackQueryHandler(helpbtn, pattern=r"help_(.*?)"))
    application.add_handler(CallbackQueryHandler(help_home, pattern=r"helphome"))

    # Sudoers
    application.add_handler(
        CommandHandler(
            "addsudo",
            addsudo,
            filters=filters.Chat(NETWORK)
            & filters.ChatType.GROUPS
            & filters.REPLY
            & filters.User(get_sudoers(), allow_empty=True),
        )
    )
    application.add_handler(
        CommandHandler(
            "rmsudo",
            remove_sudo,
            filters=filters.Chat(NETWORK)
            & filters.ChatType.GROUPS
            & filters.REPLY
            & filters.User(get_sudoers(), allow_empty=True),
        )
    )

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
