import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText


def sendMail(uid, ptEmail):
    link = "127.0.0.1:5000/patient/vidcall/" + uid

    message = EmailMessage()
    message["Subject"] = "Clinic 24/365 - Link to Online Consultation"
    message["From"] = "web.clinic.24.365@gmail.com"
    message["To"] = ptEmail

    # Change "To" to change sender (Become dynamic in actual code)

    message.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1>CLINIC 24/365</h1>
            <br>
            <p>This is the link to your online consultation.</p>
            <p>Click on the link at the bottom of the email on your phone or computer.</p>
            <br>
            <p>Please enter the call as soon as this email is received.</p>
            <p>Your booking will be dismissed if you do not enter the call within 5 minutes of the delivery of this email</p>
            <br>
            <p>Otherwise, if you would like to cancel your booking, click <a>here</a>.</p>
            <br>
            <p>This is an automated message. Do not reply.</p>
        </body>
    </html>
    """ + '<a href="' + link + '">link is here</a><br>Password: ' + uid, subtype="html")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, 'user', timeout=120) as smtp:

        smtp.login('web.clinic.24.365@gmail.com', 'Abcd1234!')
        smtp.send_message(message)


if __name__ == "__main__":
    pass
