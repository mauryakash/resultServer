from flask import Blueprint,request,render_template,session,redirect
from .models import Student
import os
import smtplib
from email.message import EmailMessage
import random
import imghdr #Image type


main = Blueprint('main', __name__)


def getOtp():
    return random.randint(1111,9999)



@main.route("/", methods=['GET','POST'])
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

            
        msg = EmailMessage()
        msg['Subject'] = 'OTP FROM Akash Server'
        msg['From'] = 'resultservertest@gmail.com'
        msg['To'] = emaildb
        x = getOtp()
        msg.set_content(str(x))
        session['response'] = str(x)  #Storing otp in session

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('resultservertest@gmail.com', os.environ.get('PASS'))
                
            smtp.send_message(msg)

        return render_template("validateotp.html",rollno = rollno)

    return render_template("home.html")



@main.route("/validateotp/<int:rollno>", methods=['POST'])
def validateotp(rollno):
    if request.method == 'POST':

        data = Student.query.get(rollno)
        emaildb = data.email 
        # mathmark=data.math_marks
        # engmark=data.english_marks

        html = render_template('resultdata.html',data=data)

        userotp = request.form['otp']

        if 'response' in session: #Checking for response in session
            s = session['response']
            session.pop('response',None)
            if s == str(userotp):

                # if  otp == int(userotp):
                msg = EmailMessage()
                msg['Subject'] = 'Mail from akash server'
                msg['From'] = 'resultservertest@gmail.com'
                msg['To'] = emaildb
                # msg.set_content(html)
                html_msg = html
                # html_msg = open('templates/resultdata.html').read()
                msg.add_alternative(html_msg, subtype='html')

                with open('app/static/fynd.jpeg','rb') as attach_file:
                    image_name = attach_file.name
                    image_type = imghdr.what(attach_file.name)
                    image_data = attach_file.read()

                msg.add_attachment(image_data, maintype='image',subtype=image_type,filename=image_name)


                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('resultservertest@gmail.com', os.environ.get('PASS'))
                        
                    smtp.send_message(msg)

                # return render_template("endpage.html",message="Check your mail for the result")
                return redirect("/endpage")
            return render_template("home.html", msg = "Otp not verified Wrong OTP!")
        return render_template("home.html", msg = "Session Expired (Otp Already Used) Try again !")
    



@main.route("/endpage", methods=['GET'])
def endpage():
    return render_template("endpage.html",message="Check your Email for the result")

