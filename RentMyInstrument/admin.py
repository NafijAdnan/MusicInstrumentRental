from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Instrument, Coupon
from functools import wraps
from sqlalchemy import desc

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.email.split('@')[1] == 'rental.admin':
                return f(*args, **kwargs)
            else:
                return redirect(url_for('views.home'))
        else:
            return redirect('/')
    return decorated_function


@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin_dashboard.html', user=current_user)


@admin.route('/manage_users')
@login_required
@admin_required
def manage_users():
    users = User.query.filter_by(isAdmin=False).order_by(User.username).all()
    return render_template('users_index.html', users=users)


@admin.route('/manage_instruments')
@login_required
@admin_required
def manage_instruments():
    instruments = Instrument.query.order_by(desc(Instrument.approval)).all()
    return render_template('manage_instruments.html', instruments=instruments)


@admin.route('/add_promo', methods=['GET', 'POST'])
@login_required
@admin_required
def add_promo():
    if request.method == 'POST':
        code = request.form.get('code')
        duration = request.form.get('duration')
        validity = request.form.get('validity')
        new_coupon = Coupon(code=code, duration=duration, validity=validity)
        db.session.add(new_coupon)
        db.session.commit()
        flash('Coupon has successfully been created!', category='success')

    return render_template('create_coupon.html')


@admin.route('/ban_user/<username>')
@login_required
@admin_required
def ban_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    flash('User has been banned.', category='error')

    return redirect(url_for('admin.manage_users'))


@admin.route('/approve_instrument/<int:id>')
@login_required
@admin_required
def approve(id):
    instrument = Instrument.query.filter_by(id=id).first()
    instrument.approval = 'Approved'
    db.session.commit()
    flash('Upload request has been approved.', category='success')

    return redirect(url_for('admin.manage_instruments'))


@admin.route('/reject_instrument/<int:id>')
@login_required
@admin_required
def reject(id):
    instrument = Instrument.query.filter_by(id=id).first()
    instrument.approval = 'Rejected'
    db.session.commit()
    flash('Upload request has been Rejected.', category='error')

    return redirect(url_for('admin.manage_instruments'))


