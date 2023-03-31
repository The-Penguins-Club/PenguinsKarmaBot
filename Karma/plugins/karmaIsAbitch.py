from pyrogram import filters

from Karma import Karma
from Karma.utils.dbhelpers import User, MonthYear, Karma as KarmaDB, get_month_year
from re import findall

karma_plus = f"^(?:\+\+|\+)?(\d+)"


@Karma.on_message(filters.regex(karma_plus) & filters.reply)
async def pluskarma(_, message):
    from_user, to_user = message.from_user, message.reply_to_message.from_user

    if not from_user or not to_user:
        return
    try:
        user = User.get(User.user_id == to_user.id)
    except Exception:
        user = User.create(user_id=to_user.id)
    try:
        month = MonthYear.get(MonthYear.id==get_month_year())
    except Exception:
        MonthYear.create()
        month = MonthYear.get(MonthYear.id==get_month_year())
    karmanum = findall(karma_plus,message.text)[0]
    if from_user.id == to_user.id:
        karma = KarmaDB.create(user = user,month_id=month,karma=karmanum*-1)
        return await message.reply("Lamo.")
    karma = KarmaDB.create(user = user,month_id=month,karma=karmanum)
    await message.reply(karma)