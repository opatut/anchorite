from anchorite import app, db, login_manager
from flask import render_template, request, redirect, url_for, abort, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType, UserUnit, GameState, AttackAction
from random import randint

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            #Login Sucesss
            login_user(user)
            return redirect(url_for('index'))
        else:
            print("Error wrong password or username")

    return render_template('login.html', register=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, password)
        db.session.add(user)
        db.session.commit()

    return render_template('login.html', register=True)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('index'))

@app.route('/game_state')
@login_required
def game_state():
    state = {
        "name": current_user.name,
        "tick": GameState.query.get(0).tick,
        "inventory": list(map(UserItem.to_json, current_user.items)),
        "units": list(map(UserUnit.to_json, current_user.units)),
        "actions": [action.to_json() for action in current_user.actions],
        "incoming_attacks": [attack.to_json() for attack in current_user.incoming_attacks]
    }

    return jsonify(state)

@app.route('/types')
@login_required
def types():
    return jsonify(dict(
        item_types = list(map(ItemType.to_json, ItemType.query.all())),
        recipes = list(map(Recipe.to_json, Recipe.query.all())),
        unit_types = list(map(UnitType.to_json, UnitType.query.all())),
        friends = [friend.to_json() for friend in current_user.friends],
        current_user = current_user.to_json()
        ))

@app.route('/action/brew', methods=['GET', 'POST'])
@login_required
def action_brew():
    recipe = Recipe.query.get_or_404(request.form['recipe_id'])

    for item in recipe.recipe_items:
        current_user.remove_item(item.item_type_id)

    current_user.queue_action(BrewAction(recipe=recipe), recipe.duration)

    db.session.commit()

    return game_state()

@app.route('/action/collect', methods=['GET', 'POST'])
@login_required
def action_collect():
    current_user.queue_action(CollectAction(), 5)
    db.session.commit()
    return game_state()

@app.route('/action/attack', methods=['GET', 'POST'])
@login_required
def action_attack():
    # get the data
    target_user_id = int(request.form['target_user_id'])
    unit_ids = request.form['unit_ids'].split(',')

    # get the models
    target_user = User.query.get_or_404(target_user_id)
    units = [UserUnit.query.get_or_404(unit_id) for unit_id in unit_ids]

    # really? attack yourself?
    if target_user_id == current_user.id:
        abort(404)

    for unit in units:
        # only send units you own, bastard!
        if unit.user != current_user:
            abort(404)

        # don't send one unit on two missions at the same time :D
        if unit.attack_action:
            abort(404)

    # duration depends on amount of units you send
    duration = len(units)**0.6 * randint(30, 50)

    # make an action
    action = AttackAction()
    action.units = units
    action.target_user = target_user

    # queue it (it will be detected as immediate starting)
    current_user.queue_action(action, duration)

    db.session.commit()
    return game_state()

@app.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    username = request.form['username']
    user = User.query.filter_by(name=username).first_or_404()

    if current_user == user:
        abort(404)

    if user in current_user.friends:
        return jsonify(ok=True)

    current_user.friends.append(user)
    db.session.commit()
    return jsonify(ok=True)

