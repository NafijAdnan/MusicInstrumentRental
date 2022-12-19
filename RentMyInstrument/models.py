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
    orders = db.relationship('Order')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), default='Active')
    product = db.Column(db.Integer, db.ForeignKey('instrument.id'))
    user = db.Column(db.String(20), db.ForeignKey('user.username'))
    delivery = db.Column(db.String(20), default='In Progress')


# class Payment(db.Model):
    pass


class Coupon(db.Model):
    code = db.Column(db.String(15), primary_key=True)
    condition = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    validity = db.Column(db.Date)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('instrument.id'))


