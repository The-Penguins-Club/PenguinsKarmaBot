from telegram import Update
from telegram.ext import ContextTypes

from bot.models import Karma, User
from httpx import get


async def increment_karma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Please reply to a message to increment karma."
        )
    reciever = update.message.reply_to_message.from_user
    sender = update.message.from_user

    if not reciever:
        return await update.message.reply_text("Cannot increment karma for this user.")

    if reciever.id == sender.id:
        return await update.message.reply_text("You cannot increment your own karma.")

    _reciever, _ = User.get_or_create(id=reciever.id)
    _sender, _ = User.get_or_create(id=sender.id)
    print(f"{_reciever}, {_sender}")
    Karma.create(user=_reciever, sender=_sender, karma=1)
    return await update.message.reply_text(
        f"Karma incremented by: 1.\nCurrent Karma Count is: {_reciever.karma}"
    )


async def decrement_karma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Please reply to a message to increment karma."
        )
    reciever = update.message.reply_to_message.from_user
    sender = update.message.from_user

    if reciever.id == sender.id:
        return await update.message.reply_text("You cannot decrement your own karma.")

    if not reciever:
        return await update.message.reply_text("Cannot decrement karma for this user.")
    _reciever, _ = User.get_or_create(id=reciever.id)
    _sender, _ = User.get_or_create(id=sender.id)
    print(f"{_reciever}, {_sender}")
    Karma.create(user=_reciever, sender=_sender, karma=-1)
    return await update.message.reply_text(
        f"Karma decremented by: 1.\nCurrent Karma Count is: {_reciever.karma}"
    )


async def karma_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = User.select(User.id, User.karma).order_by(-User.karma).limit(15)

    message_text = (
        get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        .json()
        .get("joke")
    )

    reply = await update.message.reply_text(message_text)

    message_text = "Stats:\n\n"

    bot = context.bot

    for user in users:
        chat = await bot.get_chat(user.id)
        name = chat.first_name
        if chat.last_name:
            name += f" {chat.last_name}"

        message_text += f"{name}: {user.karma}\n"

    await reply.edit_text(message_text)


async def reward_karma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Please reply to a message to reward karma."
        )
    reciever = update.message.reply_to_message.from_user
    sender = update.message.from_user

    reward_point = update.message.text.split()
    if len(reward_point) != 2 or not reward_point[1].isdigit():
        return await update.message.reply_text(
            "Usage: /reward <points>\nExample: /reward 5"
        )

    if not reciever:
        return await update.message.reply_text("Cannot reward karma for this user.")

    _reciever, _ = User.get_or_create(id=reciever.id)
    _sender, _ = User.get_or_create(id=sender.id)
    Karma.create(user=_reciever, sender=_sender, karma=int(reward_point[1]))
    return await update.message.reply_text(
        f"Karma rewarded by: {reward_point[1]}.\nCurrent Karma Count is: {_reciever.karma}"
    )


async def give_karma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Please reply to a message to give karma."
        )
    reciever = update.message.reply_to_message.from_user
    sender = update.message.from_user

    give_point = update.message.text.split()
    if len(give_point) != 2 or not give_point[1].isdigit():
        return await update.message.reply_text(
            "Usage: /give <points>\nExample: /give 5"
        )

    give_point = abs(int(give_point[1]))

    if not reciever:
        return await update.message.reply_text("Cannot give karma for this user.")

    _reciever, _ = User.get_or_create(id=reciever.id)
    _sender, _ = User.get_or_create(id=sender.id)

    if _reciever.id == _sender.id:
        return await update.message.reply_text("You cannot give karma to yourself.")

    if give_point > _sender.karma:
        return await update.message.reply_text(
            f"You don't have enough karma to give. Your current karma is {_sender.karma}."
        )

    Karma.create(user=_reciever, sender=_sender, karma=give_point)
    Karma.create(user=_sender, sender=_sender, karma=-give_point)
    return await update.message.reply_text(
        f"Karma given by: {give_point}.\nCurrent Karma Count is: {_reciever.karma}"
    )
