import os

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

@app.route("/")
def index():
  msg = Message('Hello from the other side!',
                sender=('Peter from Mailtrap', 'peter@mailtrap.io'),
                recipients=['paul@mailtrap.io'])

  msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
  msg.html = "<strong>Hey Paul</strong>, sending you this email from my <em>Flask</em> app, lmk if it works"

  mail.send(msg)

  return "Message sent!"

if __name__ == '__main__':
   app.run(debug = True)
