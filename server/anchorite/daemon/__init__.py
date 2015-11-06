from anchorite import manager, db
from anchorite.common.models import User

@manager.command
def daemon():
    #while True:
    print(User.query.all())


