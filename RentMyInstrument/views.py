from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Instrument

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('base.html')

@views.route('/test')
def test():
    return render_template('home.html')

@views.route('/test2')
def test2():
    return render_template('index.html')

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        pass
    else:
        first_name = current_user.first_name
        last_name = current_user.last_name
        username = current_user.username
        dob = current_user.dob
        email = current_user.email
        contact = current_user.contact
    return render_template('profile.html', user=current_user)

@views.route('/upload_instrument', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        model = request.form.get('model')
        brand = request.form.get('brand')
        type = request.form.get('type')
        color = request.form.get('color')
        duration = request.form.get('duration')
        location = request.form.get('location')

        new = Instrument(model=model, type=type, 
                        color=color, duration=duration, 
                        location=location)
        db.session.add(new)
        db.session.commit()
    return render_template('upload_instrument.html', user=current_user)

@views.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    if request.method == 'POST':
        if request.form.get('old_pass') == current_user.password:
            new_pass = request.form.get('new_pass')
            confirm = request.form.get('confirm')
            if new_pass == confirm:
                current_user.password = new_pass
                db.session.commit()
                flash('Password updated successfully!', category='success')
            else:
                flash('Passwords do not match! Try again.', category='error')
        else:
            flash('Incorrect Password!', category='error')
    return render_template('change_password.html', user=current_user)

