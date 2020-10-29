
from itsdangerous import URLSafeTimedSerializer
from flaskapp2 import app
from flask_mail import Message
from flaskapp2 import app
import smtplib
from twilio.rest import Client
import os


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    email = os.environ['MY_EMAIL']
    password = os.environ['MY_PASSWORD']
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email, password)

        msg = f'Subject: {subject}\n\n{template}'
        smtp.sendmail(email, to, msg)

def generateOTP(phno):
    try:
        account_sid = os.environ['account_sid']
        auth_token = os.enviorn['auth_token']
        client = Client(account_sid, auth_token)
        n = random.randint(1000, 9999)
        message = client.messages \
            .create(
            body='OTP is - ' + str(n),
            from_=  os.environ['my_number'],
            to= str(phno)
        )

        print(message.sid)
        return n
    except twilio.base.exceptions.TwilioRestException:
        flash('Invalid Mobile number','danger')
        return redirect(url_for('mobileform'))
