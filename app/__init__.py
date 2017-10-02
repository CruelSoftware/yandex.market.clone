from flask import Flask

#from app.models import User
from config import config
from .market import market as market_blueprint
from flask_admin import Admin

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
#from flask_admin.contrib.sqla import ModelView

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(market_blueprint)
    bootstrap.init_app(app)
    db.init_app(app)

    #admin = Admin(app, name='microblog', template_mode='bootstrap3')
    #admin.add_view(ModelView(User, models.session))
    return app