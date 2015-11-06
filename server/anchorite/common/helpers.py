from anchorite import manager, db

@manager.command
def init(seed=False):
    db.drop_all()
    db.create_all()

    if seed:
        pass

    db.session.commit()
