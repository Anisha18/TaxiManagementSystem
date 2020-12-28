from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CustomerRegistrationForm, AddTaxisForm, BookCabForm, CustLoginForm
from app.models import User, Customer, Cab, BookCab


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registerowner', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, contact=form.contact.data, address=form.address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/custlogin', methods=['GET', 'POST'])
def custlogin():
    if current_user.is_authenticated:
        return redirect(url_for('customer'))
    form = CustLoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('custlogin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('custhome')
        return redirect(next_page)
    return render_template('custlogin.html', title='Sign In', form=form)


@app.route('/custlogout')
def custlogout():
    logout_user()
    return redirect(url_for('custhome'))


@app.route('/customer', methods=['GET', 'POST', 'PUT', 'DELETE'])
def regcust():
    if current_user.is_authenticated:
        return redirect(url_for('custhome'))
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data, phno=form.phno.data, mailid=form.mailid.data, gender=form.gender.data, caddress=form.caddress.data)
        customer.set_password(form.password.data)
        db.session.add(customer)
        db.session.commit()
        flash('Thank you, your account have been registered with BookIt!')
        return redirect(url_for('custlogin'))
    return render_template('registercustomer.html', title='Register Customer', form=form)


@app.route('/cabs', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cabs():
    form=AddTaxisForm()
    if form.validate_on_submit():
        cab =  Cab(dname=form.dname.data, Vno=form.Vno.data, Vtype=form.Vtype.data, From=form.From.data, To=form.To.data, phone=form.phone.data, flag=0, owner_id=current_user.id)
        db.session.add(cab)
        db.session.commit()
        flash('The details of the vehicle has been added successfully!')
        return redirect(url_for('index'))
    return render_template('addtaxi.html', title='Add Taxi', form=form)


@app.route('/custhome', methods=['GET','POST'])
def custhome():
    return render_template('custhome.html', title='Customer Home')


@app.route('/check', methods=['GET','POST'])
def check():
    taxi = Cab.query.filter_by(flag=0).all() 
    results = [
                {
                    "dname":one.dname,
                    "Vno":one.Vno,
                    "Vtype":one.Vtype,
                    "From":one.From,
                    "To":one.To,
                    "phone":one.phone
                    } for one in taxi]
    return render_template('check.html', title='Check Availability', results=results) 


@app.route('/bookcab/<dname>/<Vno>/<Vtype>/<From>/<To>/<phone>', methods=['GET','POST'])
def bookcab(dname,Vno,Vtype,From,To,phone):
    form = BookCabForm()
    if form.validate_on_submit():
        obj = Cab.query.filter_by(Vno=Vno).first() 
        cust_id = Customer.query.filter_by(name=form.yname.data).first()
        bcab = BookCab(dname=dname, Vno=Vno, Vtype=Vtype, From=From, To=To, phone=phone, yname=form.yname.data, Bdate=form.Bdate.data, Btime=form.Btime.data, cab_id=obj.id, customer_id=cust_id.id) 
        obj.flag=1
        db.session.add(bcab)
        db.session.commit()
        flash('Thank You, your taxi has been booked with BookIt!')
        return redirect(url_for('custhome'))
    return render_template('bookcab.html', title='Book Taxi', dname=dname, Vno=Vno, Vtype=Vtype, From=From, To=To, phone=phone, form=form)


