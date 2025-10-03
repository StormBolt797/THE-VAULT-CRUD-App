from . import db
from flask_login import UserMixin
# no explanation needed..two dtabases one for users and other for their files and has 5 or 6 columns each as specified below
class Userfiles(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     filenames = db.Column(db.String(1000))
     datas = db.Column(db.LargeBinary() )
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    firstname = db.Column(db.String(150))
    password = db.Column(db.String(150))
    phoneno = db.Column(db.Integer,unique = True) 
    files = db.relationship('Userfiles')