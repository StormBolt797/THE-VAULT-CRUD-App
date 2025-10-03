from .auth import login
from flask import Blueprint, render_template, request, session
from flask import Flask, render_template, request, send_file
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,login_required,logout_user,current_user
from . import db
from flask import  flash
from .models import Userfiles
from .auth import login
import datetime
views = Blueprint('views',__name__)

@views.route('/',methods = ['GET','POST'])
@login_required
def home():# similar to signup in auth.py..refer that
    if request.method =="POST":
        file = request.files['file']
       # m = request.files['email']
        upload = Userfiles(filenames = file.filename,datas=file.read(),user_id = session.get('m',None))
        db.session.add(upload)#file.read reads the content in the file
        db.session.commit()
        return f'Uploaded:ss {file.filename}'
    return render_template("home.html",user = current_user)

@views.route('/fileupload',methods = ['GET','POST'])
@login_required
def fileupload():
    if request.method =="POST":
        print("ello")
        file = request.files['file']
        #up- im accessing the submitted file from server
        # ikm going to upload the above accessed dat to the datbase
       # m = request.files['email']
        upload = Userfiles(filenames = file.filename,datas=file.read(),user_id = session.get('m',None))
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {file.filename}.. Go back to home page by hitting the back button on chrome.. im not gonna spend time on creating a back button'
    return render_template("fileupload.html",user = current_user)

@views.route('/download', methods = ['GET','POST'])
@login_required
def download():       
        u = Userfiles.query.filter_by(user_id= session.get("m",None)).all()
        if request.method == "POST":
            n = int(request.form.get('filename')) # basically..there are m no.of files and the website asks for kth file to download and k is n
            return send_file(BytesIO(u[n-1].datas), download_name=u[n-1].filenames, as_attachment=True)# downloads nth file as given by the user

        if len(u) != 0:
           flash('You have '+ str(len(u))+' files')
           for i in range(len(u)):
                flash('file '+ str(i+1)+' is '+u[i].filenames)
           return render_template("download.html",user = current_user)

@views.route('/delete', methods = ['GET','POST'])
@login_required
def delete():       
        u = Userfiles.query.filter_by(user_id= session.get("m",None)).all()
        if request.method == "POST":
            n = int(request.form.get('filename')) 
            db.session.delete(u[n-1])# deletes the file
            db.session.commit()#saves
            flash("record successfully deleted!")
            return render_template("home.html",user = current_user)

        if len(u) != 0:
           flash('You have '+ str(len(u))+' files')
           for i in range(len(u)):
                flash('file '+ str(i+1)+' is '+u[i].filenames)
           return render_template("delete.html",user = current_user)
@views.route('/notes', methods = ['GET','POST'])
def notes():
     time = datetime.datetime.now()#datetime module is used to import date and time as a stamp for each notes
     if request.method == "POST":
        try:
            f = open(str(session.get('m',None))+'.txt','a')
            a = request.form.get("note")
            f.write(str(time)+':  '+a)# appends notes with timestamp eahc time
            f.writelines('\n')
            f.close()
        except FileNotFoundError:
            f = open(str(session.get('m',None))+'.txt','w')
            a = request.form.get("note")
            f.write(str(time)+':  '+a + '\n')
            
            f.close()
        u = Userfiles.query.filter_by(filenames = str(session.get('m',None))+'.txt').first()
        print(u)
        if u:
            db.session.delete(u)
            db.session.commit()
            # it appends on a new file and then deletes old file 
        f = open(str(session.get('m',None))+'.txt','r')
        a =''
        try:
            m = f.readlines()# read the contents fo the text file line by line, eahc line as an element in a list
            for i in m:
                a = a + i
        except:
            print("")
        upload = Userfiles(filenames = str(session.get('m',None))+'.txt',datas=bytes(a, encoding='utf-8'),user_id = session.get('m',None))
        db.session.add(upload)# add this notefile to database
        f.close()
        db.session.commit()
      
        flash("Note posted and updated! You can download it now!")
        return render_template('home.html',user = current_user)
     return render_template('notes.html',user = current_user)

