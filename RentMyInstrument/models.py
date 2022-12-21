from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    username = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact = db.Column(db.String(14), unique=True)
    uploads = db.relationship('Instrument', foreign_keys='Instrument.user', lazy='dynamic', cascade='all, delete-orphan')
    isAdmin = db.Column(db.Boolean, default=False)
    address = db.Column(db.String(80))
    dob = db.Column(db.Date)
    orders = db.relationship('Order', foreign_keys='Order.user')
    def get_id(self):
        return self.email


class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    location = db.Column(db.String(50))
    type = db.Column(db.String(20))
    color = db.Column(db.String(15))
    price = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    approval = db.Column(db.String(8), default='Pending')
    user = db.Column(db.String(20), db.ForeignKey('user.username'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    availability = db.Column(db.String(15), default='Available')
    # orders = db.relationship('Order')
    cart = db.relationship('Cart', primaryjoin="Cart.product==Instrument.id")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), default='Active')
    product = db.Column(db.Integer, db.ForeignKey('payment.product'))
    user = db.Column(db.String(20), db.ForeignKey('user.username'))
    delivery = db.Column(db.String(20), default='Processing')
    pay_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    pay_by = db.Column(db.String(10))
    amount = db.Column(db.Integer)
    client = db.Column(db.String(20), db.ForeignKey('instrument.user'))
    model = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    duration = db.Column(db.Integer)
    paid = db.Column(db.Boolean, default=False)
    user_contact = db.Column(db.String(14))
    user_address = db.Column(db.String(80))
    client_contact = db.Column(db.String(14))
    client_address = db.Column(db.String(80))


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery = db.Column(db.String(20), default='Home Delivery')
    # method = db.Column(db.String(20))
    product = db.Column(db.Integer, db.ForeignKey('instrument.id'))
    # product = db.Column(db.Integer)
    # voucher = db.Column(db.String(15), db.ForeignKey('coupon.code'))
    voucher = db.Column(db.String(15))
    cart_id = db.Column(db.Integer)


class Coupon(db.Model):
    code = db.Column(db.String(15), primary_key=True)
    condition = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    validity = db.Column(db.Date)
    # claimed = db.relationship('Payment')
    # claimed = db.relationship('Payment', foreign_keys='Payment.voucher')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('instrument.id'))
    # pays = db.relationship('Payment', primaryjoin="Payment.product==Cart.product")
    

