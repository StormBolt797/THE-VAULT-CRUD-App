#importing modules
from flask import Flask # flask(backend development software) import 
from flask_sqlalchemy import SQLAlchemy #importing database
from flask_login import LoginManager # gives u control over the logged in user..aslo used to authenticate

db = SQLAlchemy()#databse establish

DB_NAME= "database.db"# datbase name  = database

def create_app():#creates the website using flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sid'#useless unless we are going to publish iot on a domain
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'# linkjing this website with database called database.db
    db.init_app(app)# initialise or create the website and sets it to a variabel called app


    from .views import views # imports functions from view.py
    from .auth import auth# imports functions from auth.py

    app.register_blueprint(views, url_prefix='/') #the below two says that.. auth and view will have access to the website whatver page we are in and can access the pages in between
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Userfiles
    # creates database if its not already there
    with app.app_context():
        print("hi")
        db.create_all()# database created
    
    login_manager = LoginManager()# use 'login manager module to keep the user logged in'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # this sets an unique id for each use
    return app
