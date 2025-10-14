import logging
from typing import List, Optional

import environ
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.plugins.misc import backup,  help_command, start
from Karma.utils.dbhelpers import User

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
env = environ.Env()
environ.Env.read_env("config.env")
SUDOERS: List[int] = list(map(int, env("SUDOERS").split()))

for user in User.select().where(User.is_sudo):
    if user.user_id not in SUDOERS:
        SUDOERS.append(user.user_id)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(env("BOT_TOKEN")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        CommandHandler(
            "backup", backup, filters=filters.Chat(SUDOERS) & filters.ChatType.PRIVATE
        )
    )

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
