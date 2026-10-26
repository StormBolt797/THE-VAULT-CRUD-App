from . import db
from flask_login import UserMixin
import datetime
# no explanation needed..two dtabases one for users and other for their files and has 5 or 6 columns each as specified below
class Userfiles(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     filenames = db.Column(db.String(1000))
     datas = db.Column(db.LargeBinary() )
     filesize = db.Column(db.Integer, default=0)
     isdeleted = db.Column(db.Boolean, default=False)
     sharetoken = db.Column(db.String(100), nullable=True)
     shareexpires = db.Column(db.DateTime, nullable=True)
     date = db.Column(db.DateTime, default=datetime.datetime.now)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     

class Note(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     content = db.Column(db.Text)
     date = db.Column(db.DateTime, default=datetime.datetime.now)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    firstname = db.Column(db.String(150))
    password = db.Column(db.String(500))
    phoneno = db.Column(db.String(20), nullable=True) 
    files = db.relationship('Userfiles')
    notes = db.relationship('Note')
