from datetime import datetime

from peewee import (BooleanField, CharField, ForeignKeyField, IntegerField,
                    Model)

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


class MonthYear(BaseModel):
    id = CharField(primary_key = True,unique=True, default=get_month_year())


class Karma(BaseModel):
    user = ForeignKeyField(User, backref="karmas")
    month_id = ForeignKeyField(MonthYear, backref="karmas")
    karma = IntegerField(default=1)
