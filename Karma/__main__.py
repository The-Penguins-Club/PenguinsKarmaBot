from Karma import Karma, db, SUDOERS
from Karma.utils.dbhelpers import Karma as KarmaDB
from Karma.utils.dbhelpers import MonthYear, User

if __name__ == "__main__":
    karma = Karma()
    db.connect()
    # db.drop_tables([User, MonthYear, KarmaDB])
    db.create_tables([User, MonthYear, KarmaDB])
    for sudo in SUDOERS:
        try:
            user = User.get(User.user_id == sudo)
        except Exception:
            user = User.create(user_id=sudo)
        user.is_sudo = True
        user.save()
    karma.run()
