from anchorite import app
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType

from flask import render_template, json

@app.route('/')
def index():
    return render_template('index.html')


# This file is for Caro <3
@app.route('/game_state')
def game_state():
    state = {
        "name" : "Peter"
    }
    return json.dumps(state)

@app.route('/types')
def types():
    item_types = list(map(ItemType.to_json, ItemType.query.all()))
    recipes = list(map(Recipe.to_json, Recipe.query.all()))
    
    return json.dumps(dict(item_types=item_types, recipes=recipes))