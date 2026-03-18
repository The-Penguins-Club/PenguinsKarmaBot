if __name__ == "__main__":
    from bot import main
    from bot.database import db
    from bot.models import Karma, User

    db.connect()
    db.create_tables([User, Karma])
    main()
