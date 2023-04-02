from Karma import Karma, db
from Karma.utils.dbhelpers import Karma as KarmaDB
from Karma.utils.dbhelpers import MonthYear, User

if __name__ == "__main__":
    karma = Karma()
    db.connect()
    # db.drop_tables([User, MonthYear, KarmaDB])
    db.create_tables([User, MonthYear, KarmaDB])
    karma.run()
