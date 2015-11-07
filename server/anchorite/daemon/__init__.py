import time
from anchorite import manager, db
from anchorite.common.models import User, Action

@manager.command
def daemon():
    start_time = time.time()
    game_state = GameState.query.get(0)
    while True:
        game_state.tick += 1
        for action in Action.query.all():
            action.execute()
        db.session.commit()
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))
