import time
from anchorite import manager, db
from anchorite.common.models import User, Action, GameState

@manager.command
def daemon():
    start_time = time.time()
    game_state = GameState.query.get(0)
    while True:
        game_state.tick += 1
        for action in Action.query.filter(Action.tick <= game_state.tick).all():
            action.execute()
        db.session.commit()
        print(game_state.tick)
        time.sleep(1.0 - ((time.time() - start_time) % 1.0))
