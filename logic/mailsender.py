from smtplib import SMTPException
from flask import jsonify
from app import mail, app
from flask_mail import Message


# test function for testing flask_mail setup configurations
def test_mail():
    msg = Message(subject="GROUP MEDIA TEST MAIL",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=['groupmediaapp@gmail.com'],
                  body="This is a test email I sent with Gmail and Python!")
    mail.send(msg)
    return jsonify(message='OK'), 200


# Main sender function, fills email properties and attempts to send out an e-mail
def send_notification(recipient: str, subject: str, mail_body: str):
    msg = Message(sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient],
                  subject=subject,
                  body=mail_body)
    try:
        mail.send(msg)
        return True
    except SMTPException as err:
        print(err)
        return False


# to notify validators on an uploaded item
def upload(item_id: int):
    print(item_id)


# to notify the uploader that the uploaded item has been validated
def item_validate(item_id: int):
    print(item_id)


# to notify the uploader that the uploaded item has been rejected
def item_reject(item_id: int):
    print(item_id)


# to notify validators and other employees that an event has been cancelled
def event_cancel(event_id):
    print()


# to notify validators that an event has been finished with the list of items that belong to the finished event
def event_finish():
    print()