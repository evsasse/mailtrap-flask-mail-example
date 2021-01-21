import os

from celery import Celery
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

## https://github.com/celery/celery/issues/4081#issuecomment-408581158
## Celery may also need this, if you are running on Windows
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery = Celery(app.name, broker='redis://redis:6379/0')


def send_email(to, raw_message, html_message):
    msg = Message(
        'Hello from the other side!',
        sender=('Peter from Mailtrap', 'peter@mailtrap.io'),
        recipients=[to]
    )

    msg.body = raw_message
    msg.html = html_message

    with app.open_resource("mailtrap.png") as file:
        msg.attach("mailtrap.png", "image/png", file.read())

    with app.app_context():
        mail.send(msg)


@celery.task
def task_send_email(*args):
    send_email(*args)


@app.route("/")
def index():
    return '<a href="/sync">Sync</a> - <a href="/async">Async</a>'


@app.route("/sync")
def send_sync_email():
    send_email(
        'paul@mailtrap.io',
        'Hey Paul, sending you a Synchronous email.',
        '<strong>Hey Paul</strong>, sending you a <em>Synchronous</em> email.'
    )

    return 'Email sent Synchronously'


@app.route("/async")
def send_async_email():
    task_send_email.delay(
        'paul@mailtrap.io',
        'Hey Paul, sending you an Asynchronous email.',
        '<strong>Hey Paul</strong>, sending you an <em>Asynchronous</em> email.'
    )

    return 'Email sent Asynchronously'
