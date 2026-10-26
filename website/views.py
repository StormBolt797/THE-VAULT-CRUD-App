from .auth import login
from flask import Blueprint, render_template, request, session, redirect, url_for
from flask import Flask, render_template, request, send_file
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,login_required,logout_user,current_user
from . import db
from flask import  flash
from .models import Userfiles, Note
from .auth import login
from .crypto import encryptbytes, decryptbytes
import datetime
import uuid
views = Blueprint('views',__name__)

def userkey(uid):
    return f"vaultkey{uid}"

@views.route('/',methods = ['GET','POST'])
@login_required
def home():# similar to signup in auth.py..refer that
    uid = session.get('m', current_user.id)
    files = Userfiles.query.filter_by(user_id=uid, isdeleted=False).all()
    user_notes = Note.query.filter_by(user_id=uid).order_by(Note.date.asc()).all()
    shareurl = session.pop('share_modal_url', None)
    sharefile = session.pop('share_modal_file', None)
    if request.method =="POST":
        file = request.files['file']
       # m = request.files['email']
        raw = file.read()
        enc = encryptbytes(raw, userkey(uid))
        upload = Userfiles(filenames = file.filename,datas=enc,filesize=len(raw),user_id = uid)
        db.session.add(upload)#file.read reads the content in the file
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("home.html",user = current_user, files = files, notes = user_notes, shareurl = shareurl, sharefile = sharefile)

@views.route('/fileupload',methods = ['GET','POST'])
@login_required
def fileupload():
    uid = session.get('m', current_user.id)
    if request.method =="POST":
        print("ello")
        file = request.files['file']
        #up- im accessing the submitted file from server
        # ikm going to upload the above accessed dat to the datbase
       # m = request.files['email']
        raw = file.read()
        enc = encryptbytes(raw, userkey(uid))
        upload = Userfiles(filenames = file.filename,datas=enc,filesize=len(raw),user_id = uid)
        db.session.add(upload)
        db.session.commit()
        flash('File successfully encrypted and uploaded to your vault!', category='success')
        return redirect(url_for('views.home'))
    return render_template("fileupload.html",user = current_user)

@views.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    uid = session.get('m', current_user.id)
    f = Userfiles.query.filter_by(id=file_id, user_id=uid).first()
    if f:
        dec = decryptbytes(f.datas, userkey(uid))
        return send_file(BytesIO(dec), download_name=f.filenames, as_attachment=True)
    flash('File not found', category='error')
    return redirect(url_for('views.home'))

@views.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    uid = session.get('m', current_user.id)
    f = Userfiles.query.filter_by(id=file_id, user_id=uid).first()
    if f:
        f.isdeleted = True
        db.session.commit()
        flash('File moved to trash!', category='success')
    return redirect(url_for('views.home'))

@views.route('/trash')
@login_required
def trash():
    uid = session.get('m', current_user.id)
    trashfiles = Userfiles.query.filter_by(user_id=uid, isdeleted=True).all()
    return render_template("trash.html", user = current_user, files = trashfiles)

@views.route('/restore/<int:file_id>')
@login_required
def restore_file(file_id):
    uid = session.get('m', current_user.id)
    f = Userfiles.query.filter_by(id=file_id, user_id=uid).first()
    if f:
        f.isdeleted = False
        db.session.commit()
        flash('File restored to Vaultbox!', category='success')
    return redirect(url_for('views.trash'))

@views.route('/purge/<int:file_id>')
@login_required
def purge_file(file_id):
    uid = session.get('m', current_user.id)
    f = Userfiles.query.filter_by(id=file_id, user_id=uid).first()
    if f:
        db.session.delete(f)
        db.session.commit()
        flash('File permanently erased!', category='success')
    return redirect(url_for('views.trash'))

@views.route('/share/<int:file_id>')
@login_required
def share_file(file_id):
    uid = session.get('m', current_user.id)
    f = Userfiles.query.filter_by(id=file_id, user_id=uid).first()
    if f:
        f.sharetoken = str(uuid.uuid4())[:16]
        f.shareexpires = datetime.datetime.now() + datetime.timedelta(hours=24)
        db.session.commit()
        shareurl = url_for('views.public_file', token=f.sharetoken, _external=True)
        session['share_modal_url'] = shareurl
        session['share_modal_file'] = f.filenames
    return redirect(url_for('views.home'))

@views.route('/s/<token>')
def public_file(token):
    f = Userfiles.query.filter_by(sharetoken=token, isdeleted=False).first()
    if f:
        if f.shareexpires and datetime.datetime.now() > f.shareexpires:
            return "This share link has expired (24h limit reached).", 410
        dec = decryptbytes(f.datas, userkey(f.user_id))
        return send_file(BytesIO(dec), download_name=f.filenames, as_attachment=True)
    return "Link is invalid or has expired.", 404

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
     uid = session.get('m', current_user.id if current_user.is_authenticated else None)
     time = datetime.datetime.now()#datetime module is used to import date and time as a stamp for each notes
     if request.method == "POST":
        a = request.form.get("note")
        note_line = str(time)+':  '+a+'\n'
        u = Userfiles.query.filter_by(filenames = str(uid)+'.txt', user_id=uid).first()
        print(u)
        prev_content = ""
        if u:
            try:
                dec = decryptbytes(u.datas, userkey(uid))
                prev_content = dec.decode('utf-8')
            except:
                prev_content = ""
            db.session.delete(u)
            db.session.commit()
            # it appends on a new file and then deletes old file 
        new_content = prev_content + note_line
        rawbytes = bytes(new_content, encoding='utf-8')
        enc = encryptbytes(rawbytes, userkey(uid))
        upload = Userfiles(filenames = str(uid)+'.txt',datas=enc,filesize=len(rawbytes),user_id = uid)
        db.session.add(upload)# add this notefile to database
        db.session.commit()
      
        flash("Note posted and updated! You can download it now!")
        return redirect(url_for('views.home'))
     return render_template('notes.html',user = current_user)

@views.route('/addnote', methods=['POST'])
@login_required
def add_note():
    uid = session.get('m', current_user.id)
    text_content = request.form.get('note', '').strip()
    if text_content:
        newnote = Note(content=text_content, user_id=uid)
        db.session.add(newnote)
        db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/editnote/<int:note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    uid = session.get('m', current_user.id)
    n = Note.query.filter_by(id=note_id, user_id=uid).first()
    if n:
        newtext = request.form.get('content', '').strip()
        if newtext:
            n.content = newtext
            db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/deletenote/<int:note_id>')
@login_required
def delete_note(note_id):
    uid = session.get('m', current_user.id)
    n = Note.query.filter_by(id=note_id, user_id=uid).first()
    if n:
        db.session.delete(n)
        db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/downloadnotes')
@login_required
def download_notes():
    uid = session.get('m', current_user.id)
    allnotes = Note.query.filter_by(user_id=uid).order_by(Note.date.asc()).all()
    out = ""
    for n in allnotes:
        dt = n.date.strftime('%Y-%m-%d %H:%M:%S') if n.date else ''
        out += f"[{dt}]\n{n.content}\n\n"
    return send_file(BytesIO(out.encode('utf-8')), download_name="my_notes.txt", as_attachment=True)

@views.route('/about')
def about():
    return render_template('about.html', user = current_user)

@views.route('/contact')
def contact():
    return render_template('contact.html', user = current_user)
