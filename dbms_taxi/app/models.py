from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__='owner'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    contact = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(UserMixin, db.Model):
    __tablename__='customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phno = db.Column(db.String(64), index=True)
    mailid = db.Column(db.String(120), index=True)
    gender = db.Column(db.String(120), index=True)
    caddress = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Customer {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cab(UserMixin, db.Model):
    __tablename__='cab'

    id = db.Column(db.Integer, primary_key=True)
    dname = db.Column(db.String(64), index=True)
    Vno = db.Column(db.String(64), index=True)
    Vtype = db.Column(db.String(64), index=True)
    From = db.Column(db.String(64), index=True)
    To = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(64), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    flag = db.Column(db.Integer)

    def __repr__(self):
        return '<Cab {}>'.format(self.dname) 

class BookCab(UserMixin, db.Model):
    __tablename__='bookcab'

    id = db.Column(db.Integer, primary_key=True)
    dname = db.Column(db.String(64), index=True)
    Vno = db.Column(db.String(64), index=True)
    Vtype = db.Column(db.String(64), index=True)
    From = db.Column(db.String(64), index=True)
    To = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(64), index=True)
    yname = db.Column(db.String(64), index=True)
    Bdate = db.Column(db.String(64), index=True)
    Btime = db.Column(db.String(64), index=True)
    cab_id = db.Column(db.Integer, db.ForeignKey('cab.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __repr__(self):
        return  '<BookCab {}>'.format(self.dname)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


