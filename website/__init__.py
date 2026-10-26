#importing modules
import os
from flask import Flask # flask(backend development software) import 
from flask_sqlalchemy import SQLAlchemy #importing database
from sqlalchemy import text
from flask_login import LoginManager # gives u control over the logged in user..aslo used to authenticate

db = SQLAlchemy()#databse establish

DB_NAME= "database.db"# datbase name  = database

def create_app():#creates the website using flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sid')#useless unless we are going to publish iot on a domain
    db_url = os.environ.get('DATABASE_URL', f'sqlite:///{DB_NAME}')
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    app.config['SQLALCHEMY_DATABASE_URI']= db_url# linkjing this website with database called database.db
    db.init_app(app)# initialise or create the website and sets it to a variabel called app


    from .views import views # imports functions from view.py
    from .auth import auth# imports functions from auth.py

    app.register_blueprint(views, url_prefix='/') #the below two says that.. auth and view will have access to the website whatver page we are in and can access the pages in between
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Userfiles,Note
    # creates database if its not already there
    with app.app_context():
        print("hi")
        db.create_all()# database created
        try:
            db.session.execute(text('ALTER TABLE "user" ALTER COLUMN phoneno TYPE VARCHAR(20)'))
            db.session.execute(text('ALTER TABLE "user" ALTER COLUMN password TYPE VARCHAR(500)'))
            db.session.execute(text('ALTER TABLE userfiles ADD COLUMN IF NOT EXISTS date TIMESTAMP DEFAULT CURRENT_TIMESTAMP'))
            db.session.execute(text('ALTER TABLE userfiles ADD COLUMN IF NOT EXISTS filesize INTEGER DEFAULT 0'))
            db.session.execute(text('ALTER TABLE userfiles ADD COLUMN IF NOT EXISTS isdeleted BOOLEAN DEFAULT FALSE'))
            db.session.execute(text('ALTER TABLE userfiles ADD COLUMN IF NOT EXISTS sharetoken VARCHAR(100)'))
            db.session.commit()
        except Exception:
            db.session.rollback()
    
    login_manager = LoginManager()# use 'login manager module to keep the user logged in'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # this sets an unique id for each use
    return app
