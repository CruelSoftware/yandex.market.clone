from flask import render_template
from . import market


@market.route('/')
def index():
    return render_template('talks/index.html')


@market.route('/user/<username>')
def user(username):
    return render_template('talks/user.html', username=username)