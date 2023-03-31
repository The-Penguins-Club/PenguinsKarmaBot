from Karma import Karma, db
from Karma.utils.dbhelpers import Karma as KarmaDB, MonthYear, User

if __name__ == "__main__":
    karma = Karma()
    db.connect()
    db.create_tables([User, MonthYear, KarmaDB])
    karma.run()
