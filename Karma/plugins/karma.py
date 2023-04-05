from re import findall

from pyrogram import filters
from pyrogram.types import Message
from Karma import NETWORK, PREFIXS, SUDOERS, Karma
from Karma.utils.dbhelpers import (
    User,
    get_current_MY,
    get_karma_db,
    get_user,
    sum_of_karma,
)
from Karma.utils.filters import is_sudo, is_whitelisted

karma_re = f"^(?:\+\+|\+|\-\-|\-)?(\d+)"


async def Whole_Dmn_Thing(message, is_positive=True, is_admin=False):
    from_user, to_user = message.from_user, message.reply_to_message.from_user

    user = get_user(to_user.id)
    karma = get_karma_db(user, get_current_MY())
    karmanum = int(findall(karma_re, message.text)[0])
    if not is_positive and karmanum > 1 and not is_admin:
        return await message.reply(
            "Non admin user can't reduct karma more that 1. Sorry."
        )
    if (karmanum > 20 or karmanum < 1) and not is_admin:
        return await message.reply("Minimum Karma is 1, Max is 20. :3")
    if from_user.id == to_user.id:
        if not is_positive:
            return
        karma.karma = karma.karma - 1
        karma.save()
        return await message.reply("টুরা কোড! টুরা কোড!")
    karma.karma = karma.karma + karmanum if is_positive else karma.karma - karmanum
    karma.save()
    if is_positive:
        return await message.reply(
            f"Karma incremented by: {karmanum}.\nCurrent Karma Count is: {sum_of_karma(user)}"
        )
    await message.reply(
        f"Karma decremented by: {karmanum}.\nCurrent Karma Count is: {sum_of_karma(user)}"
    )


@Karma.on_message(
    filters.regex(karma_re)
    & filters.reply
    & filters.group
    & is_whitelisted
    & filters.chat(NETWORK)
)
async def KarmaFirm(_, message):
    if message.text.startswith("+"):
        if get_user(message.from_user.id).is_sudo or message.from_user.id in SUDOERS:
            return await Whole_Dmn_Thing(message, True, True)
        return await Whole_Dmn_Thing(message)
    elif message.text.startswith("-"):
        if get_user(message.from_user.id).is_sudo or message.from_user.id in SUDOERS:
            return await Whole_Dmn_Thing(message, False, True)
        return await Whole_Dmn_Thing(message, False)


@Karma.on_message(
    filters.command(["karmacount"], prefixes=PREFIXS)
    & is_whitelisted
    & filters.chat(NETWORK)
)
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


@Karma.on_message(filters.command(["stats"], prefixes=PREFIXS) & filters.chat(NETWORK))
async def stats(app, message: Message):
    reply = await message.reply("Checking stats!")
    stats = {user.user_id: sum_of_karma(user) for user in User.select()}
    # https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
    message_text = "Stats:\n\n"
    _limit, _current = 15, 0
    for user in stats:
        try:
            user_t = await app.get_users(int(user))
            message_text += f"{user_t.first_name}{f' {user_t.last_name}' if user_t.last_name else ''} = {stats.get(user)}\n"
            if _limit == _current:
                break
            _current += 1

        except Exception:
            user = get_user(user)
            user.delete_instance()
            print(f"Removed {user}.")
    await reply.edit_text(message_text)


def neutral(x: int):
    try:
        return x if x > 0 else x * (-1)
    except ValueError:
        return 0


@Karma.on_message(
    filters.command(["karma"], prefixes=PREFIXS)
    & is_whitelisted
    & filters.chat(NETWORK)
)
async def karma(app, message):
    if len(message.command) <= 2:
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
    filters.command("reward", prefixes=PREFIXS)
    & is_sudo
    & filters.reply
    & filters.chat(NETWORK)
)
async def Reward(_, message):
    to_user = message.reply_to_message.from_user
    if len(message.command) <= 1:
        return await message.reply("I need Two Arguments! See help section.")
    if not to_user:
        return await message.reply("I can't reward an anon user.")

    karma = get_karma_db(get_user(to_user.id), get_current_MY())
    karma.karma = karma.karma + int(float(message.command[1]))
    karma.save()
    return await message.reply(
        f"{message.from_user.mention} rewarded {to_user.mention} with {message.command[1]} Karma."
    )


@Karma.on_message(
    filters.command(["blacklist"], prefixes=PREFIXS)
    & is_sudo
    & filters.reply
    & filters.chat(NETWORK)
)
async def blacklist(_, message):
    if not message.reply_to_message.from_user:
        return await message.reply("Can't Blacklist an Anon User.")
    user = get_user(message.reply_to_message.from_user.id)
    user.is_blacklisted = True
    reason = " ".join(message.command[1:])
    user.reason_blacklist = reason
    user.save()
    return await message.reply(
        f"{message.reply_to_message.from_user.mention} has been blacklisted.\nReason is: {reason}"
    )


@Karma.on_message(
    filters.command(["rmblacklist"], prefixes=PREFIXS)
    & is_sudo
    & filters.reply
    & filters.chat(NETWORK)
)
async def rmblacklist(_, message):
    if not message.reply_to_message.from_user:
        return await message.reply("Can't UnBlacklist an Anon User.")
    user = get_user(message.reply_to_message.from_user.id)
    user.is_blacklisted = False
    reason = " ".join(message.command[1:])
    user.reason_blacklist = ""
    user.save()
    return await message.reply(
        f"{message.reply_to_message.from_user.mention} has been removed from blacklist.\nReason is: {reason}"
    )


@Karma.on_message(
    filters.command(["give", "gift"], prefixes=PREFIXS)
    & is_whitelisted
    & filters.chat(NETWORK)
)
async def donate(_, message):
    donor = message.from_user
    donordb = get_karma_db(get_user(donor.id), get_current_MY())
    recipient = message.reply_to_message.from_user
    recipientdb = get_karma_db(get_user(recipient.id), get_current_MY())
    property_of_donor = sum_of_karma(get_user(donor.id))
    donation = neutral(int(float(message.command[1])))
    if (property_of_donor - donation) < 0:
        return await message.reply("Hehe, Nice Try.")
    print(donordb.karma, recipientdb.karma)
    donordb.karma = donordb.karma - donation
    recipient.karma = recipientdb.karma + donation
    print(donor.id)
    print(donordb.karma, recipientdb.karma)
    donordb.save()
    recipientdb.save()
    return await message.reply(
        f"{donor.mention} donated {donation} ~~dollar~~karma to {recipient.mention}."
    )


@Karma.on_message(
    filters.command("addsudo", prefixes=PREFIXS) & is_sudo & filters.reply
)
async def addsudo(_, message: Message):
    future_admin = message.reply_to_message.from_user
    if not future_admin:
        return await message.reply("Anon user can't be sudo.")
    admindb = get_user(future_admin.id)
    if admindb.is_sudo:
        return await message.reply(f"{future_admin.mention} is alreay a sudo user.")
    admindb.is_sudo = True
    admindb.save()
    return await message.reply(
        f"{future_admin.mention} has been promoted to a Sudo user by {message.from_user.mention}."
    )


@Karma.on_message(
    filters.command("rmsudo", prefixes=PREFIXS) & filters.user(SUDOERS) & filters.reply
)
async def remove_sudo(_, message: Message):
    future_admin = message.reply_to_message.from_user
    if not future_admin:
        return await message.reply(
            "Anon user can't be sudo. How tf I'm supposed to remove him/her from sudo?"
        )
    admindb = get_user(future_admin.id)
    if not admindb.is_sudo:
        return await message.reply(f"{future_admin.mention} is not a sudo user.")
    admindb.is_sudo = False
    admindb.save()
    return await message.reply(
        f"{future_admin.mention} has been demoted to a regular user by {message.from_user.mention}."
    )
