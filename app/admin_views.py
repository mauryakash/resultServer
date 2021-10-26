from flask import Blueprint,session,request,render_template,redirect,flash
from .models import Student,db
import os
from flask_admin import Admin   #admin
from flask_admin.contrib.sqla import ModelView    #admin
from werkzeug.exceptions import abort    #admin

main2 = Blueprint('main2', __name__)
admin = Admin()

#-----------------------Flask admin------------------
# class SecureModelView(ModelView):
#     def is_accessible(self):
#         if "logged_in" in session:
#             return True
#         else:
#             abort(403)


# admin.add_view(SecureModelView(Student,db.session))

#--------------------------------------------------------

 #------------------------------------------------------------------------------------------------
 #-----------------------------------------Flask Admin---------------------------------------------------
 #-------------------------------------------------------------------------------------------------


# @main2.route("/login", methods=["GET","POST"])
# def login():
#     if request.method == "POST":
#         if request.form.get("username") == "test" and request.form.get("password") == "test":
#             session['logged_in'] = True
#             return redirect("/admin")
#         else:
#             return render_template("login.html", failed = True)
#     return render_template("login.html")


# @main2.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")


#----------------------------------------------------------------------------------------


@main2.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == os.environ.get('PASS'):
            session['logged_in'] = True
            return redirect("/myadmin")
        else:
            return render_template("login.html", failed = True)
    return render_template("login.html")


@main2.route("/logout" , methods=["POST"])
def logout():
    if request.method == "POST":
        session.pop('logged_in',None)
        return redirect("/login")




#-------MYAdmin--------------------------------------------------------

@main2.route("/myadmin",methods=['GET','POST'])
def add():
    if 'logged_in' in session:
            
        if request.method == 'POST':
            rollno = request.form.get('rollno')
            name = request.form.get('name')
            email = request.form.get('email')
            mobile = request.form.get('mobile')
            math_marks = request.form.get('math_marks')
            science_marks = request.form.get('science_marks')
            english_marks = request.form.get('english_marks')

            stu= Student(rollno=rollno, name=name, email=email, mobile=mobile, math_marks=math_marks, science_marks=science_marks, english_marks=english_marks)
            
            #This will Work to handle Exception IF again Same data is tried to added
            rollnodb = Student.query.get(rollno)
            if rollnodb is not None:
                flash("Roll No already Exist", "info")
                return redirect ('/myadmin')

            #Else if No Exception Then Add the data
            db.session.add(stu)
            db.session.commit()

        alldata = Student.query.all()
        return render_template("index1.html",alldata=alldata)
    return redirect('/login')

@main2.route("/update/<int:rollno>" ,methods=['GET','POST'])
def update(rollno):
    if 'logged_in' in session:

        if request.method == 'POST':
            rollno = request.form.get('rollno')
            name = request.form.get('name')
            email = request.form.get('email')
            mobile = request.form.get('mobile')
            math_marks = request.form.get('math_marks')
            science_marks = request.form.get('science_marks')
            english_marks = request.form.get('english_marks')
            #object of row of the db related to rollno
            stu = Student.query.filter_by(rollno=rollno).first()

            #update new data in db
            stu.rollno = rollno
            stu.name = name
            stu.email = email
            stu.mobile = mobile
            stu.math_marks = math_marks
            stu.science_marks = science_marks
            stu.english_marks = english_marks
            db.session.add(stu)
            db.session.commit()
            return redirect("/myadmin")
        stu = Student.query.filter_by(rollno=rollno).first()
        return render_template('update.html',stu=stu)
    return redirect('/login')



@main2.route("/delete/<int:rollno>")
def delete(rollno):
    if 'logged_in' in session:

        stu = Student.query.filter_by(rollno=rollno).first()
        db.session.delete(stu)
        db.session.commit()
        return redirect("/myadmin")
    return redirect('/login')