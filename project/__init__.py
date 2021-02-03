from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

# init SQLAlchemy so we can use it later in our models
usersDB = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_BINDS"] = {"events": "sqlite:///events.sqlite"}

    usersDB.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for event parts
    from .events import events as create_events_blueprint
    app.register_blueprint(create_events_blueprint)

    return app
