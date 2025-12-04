if __name__ == "__main__":
    from bot.database import db
    from bot.models import Karma, User
    from bot import main

    db.connect()
    db.create_tables([User, Karma])
    main()
