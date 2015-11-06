from anchorite import app

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

