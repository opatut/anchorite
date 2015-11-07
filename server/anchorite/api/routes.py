from anchorite import app, db, login_manager
from flask import render_template, json, request, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType, UserUnit

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
        "name" : current_user.name,
        "tick" : 123,
        "inventory" : list(map(UserItem.to_json, current_user.items)),
        "units" : list(map(UserUnit.to_json, current_user.units)),

    }
    
    return json.dumps(state)

@app.route('/types')
def types():
    item_types = list(map(ItemType.to_json, ItemType.query.all()))
    recipes = list(map(Recipe.to_json, Recipe.query.all()))
    unit_types = list(map (UnitType.to_json, UnitType.query.all()))
    return json.dumps(dict(item_types=item_types, recipes=recipes, unit_types=unit_types))
