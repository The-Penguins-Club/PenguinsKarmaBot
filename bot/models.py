from datetime import datetime

from peewee import BooleanField, DateTimeField, ForeignKeyField, IntegerField, TextField
from playhouse.signals import Model, post_save

from bot.database import db


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    is_sudo = BooleanField(default=False)
    is_blacklisted = BooleanField(default=False)
    karma = IntegerField(default=5)
    reason_blacklist = TextField(null=True, default="")


class Karma(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    user = ForeignKeyField(User, backref="karmas")
    sender = ForeignKeyField(User, backref="sent_karmas")
    karma = IntegerField(default=1)


@post_save(sender=Karma)
def on_save_handler(model_class, instance, created):
    user = instance.user
    user.karma += instance.karma
    user.save()
