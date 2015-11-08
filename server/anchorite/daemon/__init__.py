import time, random
from anchorite import manager, db
from anchorite.common.models import User, Action, GameState, CollectAction

@manager.command
def daemon():
    game_state = GameState.query.get(0)
    start_tick = time.time() - game_state.tick
    print(game_state.tick)
    while True:
        for action in Action.query.filter(Action.end <= game_state.tick).all():
            user = action.user
            action.execute()
            db.session.delete(action)

        #time.sleep(random.uniform(0, 1))
        for user in User.query.all():
            if user.actions.count() == 0:
                user.queue_action(CollectAction(), 5)


        tick = (time.time() - start_tick)
        game_state.tick = tick
        db.session.commit()

        print("Tick: {}".format(tick))
        time.sleep(0.5)
