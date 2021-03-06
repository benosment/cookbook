from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    # attach routes and error pages
    #  - routes are stored in app/main/views.py
    #  - error handlers are stored in app/main/errors.py
    #  - importing these modules causes the routes/errors handlers
    #    to be associated with the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
