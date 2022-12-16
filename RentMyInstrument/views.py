from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Instrument
from functools import wraps

views = Blueprint('views', __name__)


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.isAdmin == False:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('admin.dashboard'))
        else:
            return redirect('/')
    return decorated_function


@views.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.isAdmin==True:
            return redirect(url_for('admin.dashboard'))
    return render_template('base.html')


@views.route('/test')
def test():
    return render_template('test.html')


@views.route('/test2')
def test2():
    return render_template('index.html')


@views.route('/profile', methods=['GET', 'POST'])
@login_required
@user_required
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
@user_required
def upload():
    if request.method == 'POST':
        model = request.form.get('model')
        price = request.form.get('price')
        type = request.form.get('type')
        color = request.form.get('color')
        duration = request.form.get('duration')
        location = request.form.get('location')

        new = Instrument(model=model, type=type, 
                        color=color, duration=duration, 
                        price=price, location=location, user=current_user.username)
        db.session.add(new)
        db.session.commit()

        flash('Upload request submitted successfully!', category='success')
        return redirect(url_for('views.upload_history'))

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


@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    print(request.form.get)
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.dob = request.form.get('dob')
        user.address = request.form.get('address')
        user.email = request.form.get('email')
        user.contact = request.form.get('contact')
        db.session.commit()
        flash("Profile updated successfully!", category='success')

        return redirect(url_for('views.profile'))
    
    return render_template('edit_profile.html', user=current_user)


@views.route('/upload_history', methods=['GET', 'POST'])
@login_required
@user_required
def upload_history():
    uploads = Instrument.query.filter_by(user=current_user.username).all()

    return render_template('upload_history.html', user=current_user, instrument=uploads)


@views.route('/delete_instrument/<int:id>')
@login_required
@user_required
def delete(id):
    instrument = Instrument.query.filter_by(id=id).first()
    db.session.delete(instrument)
    db.session.commit()
    flash('Instrument Deleted Successfully.', category='error')

    return redirect(url_for('views.upload_history'))


@views.route('/update_instrument/<int:id>', methods=['GET', 'POST'])
@login_required
@user_required
def update_instrument(id):
    instrument = Instrument.query.filter_by(id=id).first()
    if request.method == 'POST':
        instrument.model = request.form.get('model')
        instrument.type = request.form.get('type')
        instrument.color = request.form.get('color')
        instrument.duration = request.form.get('duration')
        instrument.price = request.form.get('price')
        instrument.location = request.form.get('location')
        db.session.commit()
        flash('Instrument info updated successfully!')
        return redirect(url_for('views.upload_history'))

    return render_template('update_instrument.html', instrument=instrument)

