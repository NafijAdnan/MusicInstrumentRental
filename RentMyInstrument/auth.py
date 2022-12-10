from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = User.query.filter_by(email=email).first()
        print(user, email, password, user.isAdmin)
        if user:
            # if check_password_hash(user.password, password) and user.isAdmin == True:
            if password==user.password and user.isAdmin == True:
                print('admin')
                login_user(user, remember=True)
                return redirect(url_for('views.test'))
            # elif check_password_hash(user.password, password) and user.isAdmin == False:
            elif password==user.password and user.isAdmin == False:
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password! Try again.', category='error')
        else:
            flash('User does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        contact = request.form.get('contact')

        dup = User.query.filter_by(email=email).first()
        if dup:
            flash('User already exists!', category='error')
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
