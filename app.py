from re import template
from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy, request
from email import message
import os
import smtplib
from email.message import EmailMessage
import random


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

otp = random.randint(0000,9999)


def validate(userotp):
    if otp == int(userotp):
        return True
    



@app.route("/", methods=['GET','POST'])
def test():
    if request.method == 'POST':
        # details = request.form
        # rollno = details['rollno']
        rollno = request.form['rollno']
        data = Student.query.get_or_404(rollno,description="student does not exist")

        emaildb = data.email
           
        # subject = 'Mail from akash by server'
        # body = 'Body of email'
        # message = f'Subject: {subject}\n\n{body}'
        # # message = "this is message"

        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.login("resultservertest@gmail.com", os.environ.get('PASS'))
        # server.sendmail("resultservertest@gmail.com", emaildb , message)

            

        # msg = EmailMessage()
        # msg['Subject'] = 'Mail from akash server'
        # msg['From'] = 'resultservertest@gmail.com'
        # msg['To'] = emaildb
        # msg.set_content('This is proper email with body')

        # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        #     smtp.login('resultservertest@gmail.com', os.environ.get('PASS'))
                
        #     smtp.send_message(msg)

        # return "Check your Email for the result"


        msg = EmailMessage()
        msg['Subject'] = 'OTP FROM Akash Server'
        msg['From'] = 'resultservertest@gmail.com'
        msg['To'] = emaildb
        msg.set_content(str(otp))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('resultservertest@gmail.com', os.environ.get('PASS'))
                
            smtp.send_message(msg)

        return render_template("validateotp.html",rollno = rollno)

    return render_template("home.html")


@app.route("/validateotp/<int:rollno>", methods=['POST'])
def validateotp(rollno):
    if request.method == 'POST':

        data = Student.query.get(rollno)
        emaildb = data.email
        mathmark=data.math_marks

        render_template('resultdata.html',data=data)

        userotp = request.form['otp']
        if otp == int(userotp):

            msg = EmailMessage()
            msg['Subject'] = 'Mail from akash server'
            msg['From'] = 'resultservertest@gmail.com'
            msg['To'] = emaildb
            msg.set_content(str(mathmark))
            html_msg = open('templates/resultdata.html').read()
            msg.add_alternative(html_msg, subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('resultservertest@gmail.com', os.environ.get('PASS'))
                
                smtp.send_message(msg)

            return "Check your Email for the result"
        return render_template("home.html", msg = "Otp not verified")

 



if __name__ == '__main__':
    app.run(debug=True)
