from flask import Blueprint,request,render_template,session,redirect
from .models import Student
import os
import smtplib
from email.message import EmailMessage
import random
import imghdr #Image type
import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader

main = Blueprint('main', __name__)


def generateOtp():
    return random.randint(1111,9999)


def sendOtp(email,x):
        msg = EmailMessage()
        msg['Subject'] = 'OTP FROM Akash Server'
        msg['From'] = 'resultservertest@gmail.com'
        msg['To'] = email
        # x = generateOtp()
        msg.set_content(str(x))
        session['response'] = str(x)  #Storing otp in session

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('resultservertest@gmail.com', os.environ.get('PASS'))
                
            smtp.send_message(msg)



def encrypt_pdf(html):
    pdfkit.from_string(html,'StudentData.pdf')
    out = PdfFileWriter()
    file = PdfFileReader("StudentData.pdf")  
    # Get number of pages in original file
    num = file.numPages    
    # Iterate through every page of the original 
    # file and add it to our new file.
    for idx in range(num):        
        # Get the page at index idx
        page = file.getPage(idx)        
        # Add it to the output file
        out.addPage(page)        
    # Create a variable password and store 
    # our password in it.
    password = os.environ.get('PASS')    
    # Encrypt the new file with the entered password
    out.encrypt(password)    
    # Open a new file "myfile_encrypted.pdf"
    with open("StudentData_Encrypted.pdf", "wb") as f:        
        # Write our encrypted PDF to this file
        out.write(f)

def removePdf():
    return "StudentData_Encrypted.pdf" and "StudentData.pdf"



@main.route("/", methods=['GET','POST'])
def test():
    if request.method == 'POST':
        
        # if 'email' in session: #resend otp
        #     emaildb = session['email'] #resend otp
        #     x = generateOtp() #resend otp
        #     sendOtp(emaildb,x) #resend otp
        #     rollno = session['email']
        #     return render_template("validateotp.html",rollno = rollno)
            
        #details = request.form
        # rollno = details['rollno']
        rollno = request.form['rollno']
        data = Student.query.get_or_404(rollno,description="student does not exist")
        emaildb = data.email
        session['email'] = (emaildb,rollno) #will store this in session for resend otp

        x = generateOtp()
        sendOtp(emaildb,x)            

        return render_template("validateotp.html",rollno = rollno)

    return render_template("home.html")


@main.route("/resendotp", methods=['POST'])
def resend():
    if request.method == 'POST':
        
        if 'email' in session: #resend otp
            emaildb = session['email'][0] #resend otp
            x = generateOtp() #resend otp
            sendOtp(emaildb,x) #resend otp
            rollno = session['email'][1]
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

                encrypt_pdf(html) #call the function to generate and encrypt PDF
                # html_msg = open('templates/resultdata.html').read()
                msg.add_alternative(html_msg, subtype='html')
                
                # adding the Image Attachment
                with open('app/static/fynd.jpeg','rb') as attach_file:
                    image_name = attach_file.name
                    image_type = imghdr.what(attach_file.name)
                    image_data = attach_file.read()

                msg.add_attachment(image_data, maintype='image',subtype=image_type,filename=image_name)
                
                
                # adding the PDF Attachment
                with open("StudentData_Encrypted.pdf", 'rb') as fp:
                    pdf_data = fp.read()
                    ctype = 'application/octet-stream'
                    maintype, subtype = ctype.split('/', 1)
                    msg.add_attachment(pdf_data, maintype=maintype, subtype=subtype, filename='StudentData.pdf')
                    
                    pdfdelete = removePdf()
                    os.remove(pdfdelete)

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

