from flask import render_template, url_for,flash,redirect , request, session
from flaskapp2.form import loginForm, registerForm, TelephoneForm, otpForm, loginForm
from flaskapp2.models import User
from flaskapp2 import app, db, login_manager, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import random
import twilio
from flaskapp2.token import generate_confirmation_token, confirm_token, send_email
from datetime import date

user = User()

#Your new Phone Number is +12074642648
def generateOTP(phno):
    try:
        from twilio.rest import Client
        account_sid = 'ACdde6653e686d036a4b77ac5f402ad523'
        auth_token = '6e3b3b5f8bd09dc6c40b82340e809f19'
        client = Client(account_sid, auth_token)
        n = random.randint(1000, 9999)
        message = client.messages \
            .create(
            body='OTP is - ' + str(n),
            from_='+12074642648',
            to= str(phno)
        )

        print(message.sid)
        return n
    except twilio.base.exceptions.TwilioRestException:
        flash('Invalid Mobile number','danger')
        return redirect(url_for('mobileform'))
"""
    from twilio.rest import Client
    account_sid = 'ACdde6653e686d036a4b77ac5f402ad523'
    auth_token = '6e3b3b5f8bd09dc6c40b82340e809f19'
    client = Client(account_sid, auth_token)
    n = random.randint(1000, 9999)
    try:
        message = client.messages \
            .create(
            body="OTP : "+str(n),
            from_='+12074642648',
            to='+91' + str(phno)
        )
        return n
    except twilio.base.exceptions.TwilioRestException:
        flash('Invalid Mobile number','danger')
        return redirect(url_for('mobileform'))

"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = registerForm()
    if form.validate_on_submit():
        user.firstname=form.firstname.data
        user.lastname=form.lastname.data
        user.email=form.email.data
        user.password=form.password.data
        dob = str(form.dob.data)
        dob = dob.split('-')
        dob = date(int(dob[0]),int(dob[1]),int(dob[2]))
        user.dob = dob
        print(user.dob)
        flash('Submited successfully', 'success')
        return redirect(url_for('mobileform'))
    return render_template('index.html',title="Register", form = form)

@app.route('/generate-otp/', methods = ['GET', 'POST'])
def mobileform():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = TelephoneForm()
    if form.validate_on_submit():
        flash('This works if your number is register on Twilio', 'info')
        number = form.number.data
        session['otp'] = generateOTP(str(number))
        if session['otp']:
            user.number = number
            flash("OTP Generated", 'info')
            return redirect(url_for('mobileConfirmation'))
        else:
            flash('Enter valid mobile number')
            return redirect(url_for('mobileform'))
    return render_template('mobileForm.html', title = "Generate OTP", form = form)

@app.route('/check-otp', methods=['GET', 'POST'])
def mobileConfirmation():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = otpForm()
    if form.validate_on_submit():
        otp = form.otp.data
        if otp == session['otp']:
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('user.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            login_user(user)
            flash('Successfully Registered', 'success')
            return redirect(url_for('account'))
        else:
            flash('OTP not matched', 'danger')
            return redirect(url_for('home'))
    return render_template('checkOTP.html', form = form, title = 'Check OTP')


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if current_user.is_authenticated:
        flash('Email is already confirmed')
        return redirect(url_for('account'))
    else:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and (user.password ==  form.password.data):
            login_user(user)
            flash('Successfully logged in !', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('account'))
        else:
            flash('Incorrect username or password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title = 'Account', query = User.query.all())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))