from flask import Blueprint,session,request,render_template,redirect
from .models import Student,db
from flask_admin import Admin   #admin
from flask_admin.contrib.sqla import ModelView    #admin
from werkzeug.exceptions import abort    #admin

main2 = Blueprint('main2', __name__)
admin = Admin()

#-----------------------admin--------------
class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


admin.add_view(SecureModelView(Student,db.session))

#--------------------------------------------------------

 #------------------------------------------------------------------------------------------------
 #-----------------------------------------Admin---------------------------------------------------
 #-------------------------------------------------------------------------------------------------


@main2.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "test" and request.form.get("password") == "test":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed = True)
    return render_template("login.html")


@main2.route("/logout")
def logout():
    session.clear()
    return redirect("/")


#----------------------------------------------------------------------------------------