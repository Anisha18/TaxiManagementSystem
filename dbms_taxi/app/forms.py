from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Customer, Cab, BookCab 
import phonenumbers

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self,contact):
        try:
            p=phonenumbers.parse(contact.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                raise ValidationError('Invalid phone number')

class CustomerRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phno = StringField('Phone Number', validators=[DataRequired()])
    mailid = StringField('Email id', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    caddress = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(self,phno):
        try:
            p=phonenumbers.parse(phno.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                raise ValidationError('Invalid phone number')


class AddTaxisForm(FlaskForm):
    dname = StringField('Driver Name', validators=[DataRequired()])
    Vno = StringField('Vehicle Number', validators=[DataRequired()])
    Vtype = StringField('Vehicle Type', validators=[DataRequired()])
    From = StringField('From', validators=[DataRequired()])
    To = StringField('To', validators=[DataRequired()])
    phone = StringField('Phone No', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_phone(self,phone):
        try:
            p=phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class BookCabForm(FlaskForm):
    Yname = StringField('Your Name', validators=[DataRequired()])
    Bdate = StringField('Date', validators=[DataRequired()])
    Btime = StringField('Time', validators=[DataRequired()])
    submit = SubmitField('Book Taxi')

