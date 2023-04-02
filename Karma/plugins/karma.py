from re import findall

from pyrogram import filters

from Karma import SUDOERS, Karma
from Karma.utils.dbhelpers import (
    User,
    get_current_MY,
    get_karma_db,
    get_user,
    sum_of_karma,
)

karma_re = f"^(?:\+\+|\+|\-\-|\-)?(\d+)"


async def Whole_Dmn_Thing(message, is_positive=True):
    from_user, to_user = message.from_user, message.reply_to_message.from_user

    if not from_user or not to_user:
        return
    user = get_user(to_user.id)
    month = get_current_MY()
    karma = get_karma_db(user, month)
    karmanum = int(findall(karma_re, message.text)[0])
    if karmanum > 20 or karmanum < 1:
        return await message.reply("Minimum Karma is 1, Max is 20. :3")
    if from_user.id == to_user.id:
        if not is_positive:
            return
        karma.karma = karma.karma - 1
        karma.save()
        return await message.reply("টুরা কোড! টুরা কোড!")
    if is_positive:
        karma.karma = karma.karma + karmanum
    else:
        karma.karma = karma.karma - karmanum
    karma.save()
    if is_positive:
        return await message.reply(
            f"Karma incremented by: {karmanum}.\nCurrent Karma Count is: {sum_of_karma(user)}"
        )
    await message.reply(
        f"Karma decremented by: {karmanum}.\nCurrent Karma Count is: {sum_of_karma(user)}"
    )


@Karma.on_message(filters.regex(karma_re) & filters.reply & filters.group)
async def KarmaFirm(_, message):
    if message.text.startswith("+"):
        return await Whole_Dmn_Thing(message)
    elif message.text.startswith("-"):
        return await Whole_Dmn_Thing(message, False)


@Karma.on_message(filters.command(["karmacount"]))
async def karmaCount(_, message):
    if message.reply_to_message:
        user_t = message.reply_to_message.from_user
    else:
        user_t = message.from_user
    try:
        user = User.get(User.user_id == user_t.id)
    except Exception:
        user = User.create(user_id=user_t.id)
    await message.reply(f"Karma Count of {user_t.mention} is {sum_of_karma(user)}")


@Karma.on_message(filters.command(["stats"]))
async def stats(app, message):
    stats = {}
    _limit, _current = 15, 0
    for user in User.select():
        stats[user.user_id] = sum_of_karma(user)
        if _limit == _current:
            break
        _current += 1

    # https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    print(stats)
    stats = dict(sorted(stats.items(), key=lambda x: x[1]), reverse=True)
    print(stats)
    message_text = ""
    for user in stats:
        user_t = await app.get_users(int(user))
        message_text += f"{user_t.mention} = {stats.get(user)}\n"
    await message.reply(message_text)


def neutral(x: int):
    if x > 0:
        return x
    return x * (-1)


@Karma.on_message(filters.command(["karma"]))
async def karma(app, message):
    if not len(message.command) > 2:
        return
    try:
        userid = await app.get_users(message.command[1])
        userid = userid.id
    except Exception:
        return await message.reply("User not Found.")

    user = get_user(userid)
    month = get_current_MY()
    karma = get_karma_db(user, month)
    karmanum = message.command[2]
    try:
        karmanum = int(float(karmanum))
    except ValueError:
        karmanum = 1

    if neutral(karmanum) > 20 or neutral(karmanum) < 1:
        return await message.reply("Minimum Karma is 1, Max is 20. :3")

    karma.karma = karma.karma + karmanum
    karma.save()
    if karmanum > 0:
        return await message.reply(
            f"Karma incremented by: {karmanum}.\nCurrent Karma Count is: {sum_of_karma(user)}"
        )
    await message.reply(
        f"Karma decremented by: {karmanum}.\nCurrent Karma Count is: {sum_of_karma(user)}"
    )


@Karma.on_message(
    filters.command("reward") & filters.user(SUDOERS) & filters.reply & filters.group
)
async def Reward(_, message):
    to_user = message.reply_to_message.from_user
    if not len(message.command) > 1:
        return await message.reply("I need Two Arguments! See help section.")
    if not to_user:
        return await message.reply("I can't reward an anon user.")

    user = get_user(to_user.id)
    month = get_current_MY()
    karma = get_karma_db(user, month)
    karma.karma = karma.karma + int(float(message.command[1]))
    return await message.reply(
        f"{message.from_user.mention} rewarded {to_user.mention} with {message.command[1]} Karma."
    )
