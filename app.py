from flask import Flask, jsonify, request,render_template
from flask_sqlalchemy import SQLAlchemy, request
from email import message
import os
import smtplib
from email.message import EmailMessage


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ram#12345@localhost/result'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    rollno = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    mobile = db.Column(db.Integer(), unique=True, nullable=False)
    math_marks = db.Column(db.Integer())
    science_marks = db.Column(db.Integer())
    english_marks = db.Column(db.Integer())



@app.route("/", methods=['GET','POST'])
def test():
    if request.method == 'POST':
        # details = request.form
        # rollno = details['rollno']
        rollno = request.form['rollno']
        data = Student.query.get(rollno)

        emaildb = data.email
           
        # subject = 'Mail from akash by server'
        # body = 'Body of email'
        # message = f'Subject: {subject}\n\n{body}'
        # # message = "this is message"

        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.login("resultservertest@gmail.com", os.environ.get('PASS'))
        # server.sendmail("resultservertest@gmail.com", emaildb , message)

            

        msg = EmailMessage()
        msg['Subject'] = 'Mail from akash server'
        msg['From'] = 'resultservertest@gmail.com'
        msg['To'] = emaildb
        msg.set_content('This is proper email with body')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('resultservertest@gmail.com', os.environ.get('PASS'))
                
            smtp.send_message(msg)

        return "Check your Email for the result"

    return render_template("home.html")



if __name__ == '__main__':
    app.run(debug=True)
