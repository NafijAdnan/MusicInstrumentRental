from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('email')
    
        user = User.query.filter_by(email=email).first()
        userid = User.query.filter_by(username=username).first()

        if user:
            # if check_password_hash(user.password, password) and user.isAdmin == True:
            if password==user.password and user.isAdmin == True:
                print('admin')
                login_user(user, remember=True)
                return redirect(url_for('admin.dashboard'))
            # elif check_password_hash(user.password, password) and user.isAdmin == False:
            elif password==user.password and user.isAdmin == False:
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password! Try again.', category='error')
        elif userid:
            # if check_password_hash(userid.password, password) and userid.isAdmin == True:
            if password==userid.password and userid.isAdmin == True:
                print('admin')
                login_user(userid, remember=True)
                return redirect(url_for('admin.dashboard'))
            # elif check_password_hash(userid.password, password) and userid.isAdmin == False:
            elif password==userid.password and userid.isAdmin == False:
                login_user(userid, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password! Try again.', category='error')
        else:
            flash('User does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        contact = request.form.get('contact')

        dup_email = User.query.filter_by(email=email).first()
        dup_username = User.query.filter_by(username=username).first()
        dup_contact = User.query.filter_by(contact=contact).first()
        
        if dup_email:
            flash('An account with this email is already registered!', category='error')
        elif dup_username:
            flash('Username already taken!', category='error')
        elif dup_contact:
            flash('An user with this contact number already exists!', category='error')
        elif '@' not in email and len(email)<5:
            flash('Invalid Email Address', category='error')
        elif len(password)<6:
            flash('Password must contain atleast 6 characters', category='error')
        elif password!=cpassword:
            flash("Passwords do not match", category='error')
        elif len(contact) != 11:
            flash('Invalid Phone Number', category='error')
        else:
            if email.split('@')[1] == 'rental.admin':
                new_user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name,
                        password=password,
                        contact=contact, isAdmin=True)
                db.session.add(new_user)
                db.session.commit()
                flash('Account successfully created!', category='success')
                return redirect(url_for('auth.login'))
            else:
                new_user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name,
                        password=password,
                        contact=contact)
                db.session.add(new_user)
                db.session.commit()
                flash('Account successfully created!', category='success')
                return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
