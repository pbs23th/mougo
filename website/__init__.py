from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'trade'


def create_app():
    app = Flask(__name__)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['SECRET_KEY'] = 'sdjfolsakjflskjflsakdjasdasf'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/trade"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 100,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .bitmex import bitmex

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(bitmex, url_prefix='/')

    from .models import User, Upbit_setting, Upbit_buyintervalset, Okex_setting, Okex_buyintervalset, okex_orderhistory, \
        okex_instrument, okex_ordidlist, upbit_orderhistory, upbit_ordidlist
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
