from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
# from flask_script import Manager
# from os import path

db = SQLAlchemy()
DB_NAME = "470_Project"

def createApp():
    app = Flask(__name__, static_url_path='/',
                static_folder='static',
                template_folder='templates')  
    app.config['SECRET_KEY'] = '20301016'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:@127.0.0.1:3306/{DB_NAME}'
    
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Instrument, Order, Coupon
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        user = User.query.filter_by(email=email).first()
        return user

    return app

# def create_database(app):
    if not path.exists('RentMyInstrument/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

