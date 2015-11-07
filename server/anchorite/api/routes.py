from anchorite import app, db, login_manager
from flask import render_template, json, request, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType, UserUnit, GameState

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
        "actions": [action.to_json() for action in current_user.actions]
    }

    return json.dumps(state)

@app.route('/types')
def types():
    item_types = list(map(ItemType.to_json, ItemType.query.all()))
    recipes = list(map(Recipe.to_json, Recipe.query.all()))
    unit_types = list(map (UnitType.to_json, UnitType.query.all()))
    return json.dumps(dict(item_types=item_types, recipes=recipes, unit_types=unit_types))

@app.route('/action_brew', methods=['GET', 'POST'])
@login_required
def action_brew():
    recipe = Recipe.query.get_or_404(request.form['recipe_id'])
    items = recipe.recipe_items
    gamestate = GameState.query.get(0)
    for item in items:
        current_user.remove_item(item.item_type_id)

    current_user.actions.append(BrewAction(recipe=recipe,start=gamestate.tick, end=gamestate.tick + recipe.duration))
    db.session.commit()
    return game_state()

@app.route('/action_collect', methods=['GET', 'POST'])
@login_required
def action_collect():
    gamestate = GameState.query.get(0)
    current_user.actions.append(CollectAction(start=gamestate.tick, end=gamestate.tick + 60))
    db.session.commit()
    return game_state()
