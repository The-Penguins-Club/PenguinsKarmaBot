from datetime import datetime

from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

from Karma import db


def get_month_year(
    year=int(datetime.now().strftime("%Y")), month=int(datetime.now().strftime("%m"))
):
    return str(datetime(year, month, 1).strftime("%B%Y"))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    user_id = IntegerField(unique=True)
    is_sudo = BooleanField(default=False)
    is_blacklisted = BooleanField(default=0)
    reason_blacklist = TextField(null=True, default="")


class MonthYear(BaseModel):
    id = CharField(primary_key=True, unique=True, default=get_month_year())


class Karma(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    user = ForeignKeyField(User, backref="karmas")
    month_id = ForeignKeyField(MonthYear, backref="karmas")
    karma = IntegerField(default=1)


def sum_of_karma(User):
    _sum = 0
    for karma in User.karmas:
        _sum = _sum + karma.karma
    return _sum


def get_user(userid):
    try:
        return User.get(User.user_id == userid)
    except Exception:
        return User.create(user_id=userid)


def get_current_MY():
    try:
        return MonthYear.get(MonthYear.id == get_month_year())
    except Exception:
        MonthYear.create()
        return MonthYear.get(MonthYear.id == get_month_year())


def get_karma_db(user, month):
    try:
        return Karma.get(Karma.user == user, Karma.month_id == month)
    except Exception:
        Karma.create(user=user, month_id=month, karma=0)
        return Karma.get(Karma.user == user, Karma.month_id == month)
