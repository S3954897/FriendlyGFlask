from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Time
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "friendlyG.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'itAlwaysWorksInTheEnd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .displays import displays
    from .auth import auth




    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(displays, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users, Shops, Displays, Advertisements, ShopAds, Items, Menus, ShopMenus, MenuItems
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
