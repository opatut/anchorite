from anchorite import app, db
from flask import render_template, json, request
from anchorite.common.models import User

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

# This file is for Caro <3
@app.route('/game_state')
def game_state():
    state = {
        "name" : "Peter"
    }
    return json.dumps(state)

