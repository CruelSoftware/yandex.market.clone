from flask import Flask

from config import config
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()


from .models import (User, Category, Object, Colors, association_table,
                     UserAdmin, CategoryAdmin, ColorsAdmin, ObjectAdmin,
                     Image, ImageView, Param, ParamAdmin, ObjectParam,
                     ObjectParamAdmin)


def create_app(config_name):
    from .market import market as market_blueprint
    from .admin import admin_panel as admin_blueprint
    import flask_admin as admin

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(market_blueprint)
    app.register_blueprint(admin_blueprint)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    admin = admin.Admin(app, name='Example: Market', template_mode='bootstrap3')
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(CategoryAdmin(Category, db.session))
    admin.add_view(ColorsAdmin(Colors, db.session))
    admin.add_view(ObjectAdmin(Object, db.session))
    admin.add_view(ImageView(Image, db.session))
    admin.add_view(ParamAdmin(Param, db.session))
    admin.add_view(ObjectParamAdmin(ObjectParam, db.session))

    # admin = Admin(app, name='microblog', template_mode='bootstrap3')
    # admin.add_view(ModelView(User, models.session))
    return app
