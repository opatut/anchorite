from anchorite import app

from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')


# This file is for Caro <3
