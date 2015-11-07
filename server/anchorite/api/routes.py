from anchorite import app, db
from flask import render_template, json, request
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            #Login Sucesss
            login_user(user)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    user = User(username, password)
    db.session.add(user)

@app.route('/game_state')
def game_state():
    state = {
        
    }
    return json.dumps(state)

@app.route('/types')
def types():
    item_types = list(map(ItemType.to_json, ItemType.query.all()))
    recipes = list(map(Recipe.to_json, Recipe.query.all()))
    unit_types = list(map (UnitType.to_json, UnitType.query.all()))
    return json.dumps(dict(item_types=item_types, recipes=recipes, unit_types=unit_types))
