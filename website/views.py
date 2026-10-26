from .auth import login
from flask import Blueprint, render_template, request, session, redirect, url_for
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
    uid = session.get('m', current_user.id)
    files = Userfiles.query.filter_by(user_id=uid).all()
    if request.method =="POST":
        file = request.files['file']
       # m = request.files['email']
        upload = Userfiles(filenames = file.filename,datas=file.read(),user_id = session.get('m',None))
        db.session.add(upload)#file.read reads the content in the file
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("home.html",user = current_user, files = files)

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
        flash('File successfully uploaded to your vault!', category='success')
        return redirect(url_for('views.home'))
    return render_template("fileupload.html",user = current_user)

@views.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    uid = session.get('m', current_user.id)
    f = Userfiles.query.filter_by(id=file_id, user_id=uid).first()
    if f:
        return send_file(BytesIO(f.datas), download_name=f.filenames, as_attachment=True)
    flash('File not found', category='error')
    return redirect(url_for('views.home'))

@views.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    uid = session.get('m', current_user.id)
    f = Userfiles.query.filter_by(id=file_id, user_id=uid).first()
    if f:
        db.session.delete(f)
        db.session.commit()
        flash('File deleted successfully!', category='success')
    return redirect(url_for('views.home'))

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
        a = request.form.get("note")
        note_line = str(time)+':  '+a+'\n'
        u = Userfiles.query.filter_by(filenames = str(session.get('m',None))+'.txt').first()
        print(u)
        prev_content = ""
        if u:
            try:
                prev_content = u.datas.decode('utf-8')
            except:
                prev_content = ""
            db.session.delete(u)
            db.session.commit()
            # it appends on a new file and then deletes old file 
        new_content = prev_content + note_line
        upload = Userfiles(filenames = str(session.get('m',None))+'.txt',datas=bytes(new_content, encoding='utf-8'),user_id = session.get('m',None))
        db.session.add(upload)# add this notefile to database
        db.session.commit()
      
        flash("Note posted and updated! You can download it now!")
        return redirect(url_for('views.home'))
     return render_template('notes.html',user = current_user)

@views.route('/about')
def about():
    return render_template('about.html', user = current_user)

@views.route('/contact')
def contact():
    return render_template('contact.html', user = current_user)


