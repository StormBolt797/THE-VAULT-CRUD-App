from flask import Blueprint, render_template, request, flash, session
from .models import User,Userfiles
from . import db
from flask import redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint('auth',__name__)# gets all the routes possible and gives access to it for auth

@auth.route('/login', methods=['GET','POST'] )# if the currrent page has "https:"some thing"/login"
def login():#this executes  get asks for data from user and posts recieves data either from user or from itself(say login form)

    if request.method == 'POST':# if some data is recieved while in the "/login page"
        email = request.form.get('email')# get email from the user form
        ppassword = request.form.get('password')# gets password
        user = User.query.filter_by(email = email).first()# checks if the given email exist in the db
        if user:#if there is at least one email already in database
            if check_password_hash(user.password, ppassword):# check password hash=> the password is already hashed..this is the only way to check..this decrypts and checks and encrypts it again
                
                flash('logged in successfully!',category='success')# flash just gives a pop up alert box
                login_user(user,remember=True)# i use login user module to keep user logged in
                session['m'] = user.id # a sessiobn is something thatis active until user logs out.. im storing the id into a variable called m
                return redirect(url_for('views.home'))# redirects to home page
            else:
                flash('incorrect password..try again..')
        else:
            flash("Email doesn't exist..Try signing in...")    
    return render_template('login.html', user = current_user)# render templates renders that html page and redirects the page

@auth.route('/fileupload')# below fn works when we are in the"/fileupload" page
def fileupload():
    return render_template('fileupload.html')# redirects to fileupload html page 

@auth.route('/download')
def download():
    return render_template('download.html')    # redirects to download page

@auth.route('/delete')# if the current page is in /delete
def delete():
    return render_template('delete.html') # redirects to delete page

@auth.route('/logout')
@login_required# we can only logout if we are already logged in, and this makes sure of that
def logout():
    logout_user()
    return redirect(url_for('auth.login'))# redirects to login page

@auth.route('/signup',methods=['GET','POST'])# checks if the current page is "/signup"
def signup():# gets from user and posts to database(ourselves)
    if request.method == 'POST':#I HAV ALREADY DID FOR LOGIN..REFER THAT
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password = request.form.get('password1')
        phonenumber = request.form.get('phoneno')
        print(email,firstname,password,phonenumber)
        print('hello')
        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email exists!try logging in..',category="error")
        elif len(email)< 5 or len(firstname)<3 or len(password) < 3 or len(phonenumber) != 10:
            flash('Make sure your details are correct: Email should be more than 4 charachters, Name and password should be more than three characters and phone number should be ten digits',category='error')
            pass
        else:
            new_user = User(email = email, firstname = firstname,password = generate_password_hash(password),phoneno =phonenumber)
            db.session.add(new_user)# this adds the user if it isnt already in database
            db.session.commit()# saves the changes
            flash("account successful",category='success')
            return redirect(url_for('auth.login'))
            pass

    return render_template('signup.html',user=current_user)# user = current user keeps the user logged in when he shifts from one page to another