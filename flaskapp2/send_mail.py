import smtplib

email = 'shreerocker12@gmail.com'
password = 'Shree@123'

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(email, password)

    sub = 'Test case'
    body = 'Testing the mail sending'
    msg = f'Subject: {sub}\n\n{body}'
    smtp.sendmail(email, email, msg)