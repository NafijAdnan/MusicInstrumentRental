from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Instrument, Cart, Payment, Coupon, Order
from functools import wraps
from sqlalchemy import desc

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


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        instrument = search()
        # return redirect(url_for('views.search'))
        return render_template('instrument_index.html', instrument=instrument)
    if current_user.is_authenticated:
        if current_user.isAdmin==True:
            return redirect(url_for('admin.dashboard'))
    return render_template('home.html')


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
        flash('Instrument info updated successfully!', category='success')
        return redirect(url_for('views.upload_history'))

    return render_template('update_instrument.html', instrument=instrument)


@views.route('/instruments', methods=['GET', 'POST'])
def instruments(sort=None):
    if sort=='asc':
        instrument = Instrument.query.filter_by(approval='Approved').order_by(Instrument.duration).all()
    elif sort=='desc':
        instrument = Instrument.query.filter_by(approval='Approved').order_by(desc(Instrument.duration)).all()
    else:
        instrument = Instrument.query.filter_by(approval='Approved').order_by(Instrument.id).all()
    if request.method=='POST':
        instrument = search()
    return render_template('instrument_index.html', instrument=instrument)


@views.route('/instruments/sort_by_duration_asc')
def sort_asc():
    sort = 'asc'
    return instruments(sort)

@views.route('/instruments/sort_by_duration_desc')
def sort_desc():
    sort = 'desc'
    return instruments(sort)


@views.route('/search', methods=['GET', 'POST'])
def search():
    search_for = request.form.get('search')
    instrument = Instrument.query.filter_by(approval='Approved').filter(Instrument.model.like(f'%{search_for}%')).all()
    instrument += Instrument.query.filter_by(approval='Approved').filter(Instrument.type.like(f'%{search_for}%')).all()
    print(search_for, instrument)
    # return render_template('instrument_index.html', instrument=instrument)
    return instrument


@views.route('/instrument/<int:id>', methods=['POST', 'GET'])
def view_instrument(id):
    instrument = Instrument.query.filter_by(id=id).first()
    contact = User.query.filter_by(username=Instrument.user).first().contact
    cart_item = Cart.query.first()
    if cart_item:
        if cart_item.product == id:
            return render_template('instrument_details.html', instrument=instrument, carted=True)
        else:
            # if request.method == 'POST':
                # return redirect(url_for('views.clear_cart'))
            return render_template('instrument_details.html', instrument=instrument, clear=True)
    else:
        if current_user.is_authenticated:
            if request.method == 'POST':
                return redirect(url_for('views.cart', id=id))
    return render_template('instrument_details.html', instrument=instrument, contact=contact)


@views.route('/cart/<int:id>', methods=['GET', 'POST'])
@login_required
def cart(id):
    instrument = Instrument.query.filter_by(id=id).first()
    cart_item = Cart(product=instrument.id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('views.view_instrument', id=id))

@views.route('/cart', methods=['GET', 'POST'])
@login_required
def show_cart():
    cart = Cart.query.first()
    if cart:
        instrument = Instrument.query.filter_by(id=cart.product).first()
    else:
        flash('Your cart is empty... Please add something first!', category='error')
        return redirect(url_for('views.home'))
    if request.method=='POST':
        my_cart = Cart.query.first()
        for item in Payment.query.all():
            if item.cart_id == my_cart.id:
                return redirect(url_for('views.checkout'))
        delivery = request.form.get('delivery')
        voucher = request.form.get('coupon')
        product = my_cart.product
        cart_id = my_cart.id
        pay = Payment(delivery=delivery, product=product, voucher=voucher, cart_id=cart_id)
        db.session.add(pay)
        db.session.commit()
        return redirect(url_for('views.checkout'))
    return render_template('cart.html', instrument=instrument)

@views.route('/clear_cart')
@login_required
def clear_cart():
    item = Cart.query.all()
    product = Cart.query.first().product
    for i in item:
        db.session.delete(i)
    db.session.commit()
    return redirect(url_for('views.instruments'))
    # return redirect(url_for('views.view_instrument', id=product))


@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.first()
    pay = Payment.query.filter_by(cart_id=cart.id).first()
    if not pay:
        return redirect(url_for('views.instruments'))
    product = Instrument.query.filter_by(id=pay.product).first()
    price = product.price
    delivery = False
    coupon = None
    if pay.delivery == 'Home Delivery':
        price += 60
        delivery = True
    if pay.voucher:
        code = pay.voucher.lower()
        coupon = Coupon.query.filter_by(code=code).first()
        if coupon in Coupon.query.all():
            price -= coupon.discount
    
    if request.method == 'POST':
        pay_by = request.form.get('payment')
        user = current_user.username
        user_contact = current_user.contact
        user_address = current_user.address
        pay_id = pay.id
        client = product.user
        client_contact = User.query.filter_by(username=client).first().contact
        client_address = User.query.filter_by(username=client).first().address
        model = product.model
        duration = product.duration
        new_order = Order(product=pay.product, user=user, pay_by=pay_by, pay_id=pay_id, amount=price,
                         client=client, model=model, user_contact=user_contact, user_address=user_address, 
                         client_contact=client_contact, client_address=client_address, duration=duration)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('views.order'))
    return render_template('checkout.html', product=product, price=price, delivery=delivery, coupon=coupon)


@views.route('/place_order')
@login_required
def order():
    flash('Your order has been placed! Please wait while the product owner reaches to you.', category='success')
    return redirect(url_for('views.rental_history'))


@views.route('/rental_history', methods=['POST', 'GET'])
@login_required
def rental_history():
    rented = Order.query.filter_by(user=current_user.username).all()
    return render_template('rental_history.html', rented=rented)


@views.route('/cancel_order/<int:id>')
@login_required
def cancel_order(id):
    order = Order.query.filter_by(id=id).first()
    order.status = 'Canceled'
    db.session.commit()
    flash('Your order has been canceled.', category='error')
    return redirect(url_for('views.rental_history'))


@views.route('/rent-away-history', methods=['GET', 'POST'])
@login_required
def rent_away_history():
    provided = Order.query.filter_by(client=current_user.username).all()
    if request.method == "POST":
        id = request.form.get('id')
        order = Order.query.filter_by(id=id).first()
        if request.form.get('paid')=='true':
            order.paid = True
        order.delivery = request.form.get('delivery')
        db.session.commit()
    return render_template('rent_away_history.html', provided=provided)

