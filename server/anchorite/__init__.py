from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.script import Manager

app = Flask(__name__)
app.config.from_pyfile("../config.py.example", silent=True)
app.config.from_pyfile("../config.py", silent=True)

manager = Manager(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

import anchorite.common.models
import anchorite.api.routes
import anchorite.daemon

