from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "friendlyG.db"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'adverts')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'itAlwaysWorksInTheEnd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    migrate.init_app(app, db)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    from .displays import displays
    from .auth import auth
    from .adsControl import adsControl

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(displays, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(adsControl, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import Users
        return Users.query.get(int(id))

    return app


def create_database():
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')
