from anchorite import manager, db
from anchorite.common.models import User, Action

@manager.command
def daemon():
    #while True:
    #print(User.query.all())

    for action in Action.query.all():
        action.execute()



