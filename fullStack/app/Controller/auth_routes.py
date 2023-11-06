from datetime import datetime
import mailbox
from flask import Flask, jsonify, render_template, flash, redirect, url_for, request, Blueprint
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
import urllib3
from app import db

from app.Controller.auth_forms import LoginForm, affiliateRegister, AddKeywords, AdminEditProfile
from app.Controller.forms import EmailForm
from app.Controller.routes import email
from app.Model.models import Affiliate, Department, Interest, Campus
from flask_login import login_user, current_user, logout_user, login_required
from config import Config
from flask_mail import Mail, Message
auth_blueprint = Blueprint('auth', __name__)
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER
import mysql.connector
# for users that do not have their email in the db

application = Flask(__name__)
# app1.config.from_object(Config)
# Flask-Mail Configuration
# Example: Outlook/Office 365 SMTP server
# https://stackoverflow.com/questions/17980351/flask-mail-not-sending-emails-no-error-is-being-reported
# https://stackoverflow.com/questions/28466384/python-flask-email-keyerror-keyerror-mail
application.config['MAIL_SERVER'] = 'smtp.office365.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_DEFAULT_SENDER'] = 'wsuaffiliateconfirmation@outlook.com'
application.config['MAIL_USERNAME'] = 'wsuaffiliateconfirmation@outlook.com'
application.config['MAIL_PASSWORD'] = 'changethislater!'
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USE_SSL'] = False

application.config['MAIL_DEBUG'] = True

application.config['MAIL_SUPPRESS_SEND'] = False
application.config['TESTING'] = False
mail = Mail(application)
#DEBUG = True
#from flask.ext.mail import Mail, Message
# Flask-Mail Configuration

s = URLSafeTimedSerializer('Thisisasecret!')


########################validate email for exisiting users

   
@auth_blueprint.route('/validateEmailDB', methods=['GET', 'POST'])
def validateEmailDB():

    form = EmailForm()  # Creating an instance of the EmailForm class

    if form.validate_on_submit():  # If the form is submitted and validated
        email = form.email.data  # Get the email entered by the user
        return redirect(url_for('auth.emailDB', givenEmail=email))

    return render_template('email_template.html', form=form)
    
@auth_blueprint.route('/emailDB/<givenEmail>', methods=['GET', 'POST'])
def emailDB(givenEmail):
    if request.method == 'GET':

        # email = request.form['email']
        print("1")
        email = givenEmail
        print(email)
        token = s.dumps(email, salt='email-confirm')
        print("2")
        msg = Message(
            'Confirm Email', sender='wsuaffiliateconfirmation@outlook.com', recipients=[email])
        print("3")
        link = url_for('auth.confirm_email_DB', token=token,
                       _external=True)  # look at later
        print("this is test\n")
        print(application.config['MAIL_SERVER'])
        print(application.config['MAIL_PORT'])
        msg.body = 'Your link is {}'.format(link)
    # msg.body="test"ws1
    # g@gmail.com

        try:
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", str(e))

       # return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
        return 'email sending...please check email'
    


@auth_blueprint.route('/confirm_email_DB/<token>')
def confirm_email_DB(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        
        return redirect(url_for('auth.registerDB', givenEmail=email))

    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

def testD(givenEmail):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="teamFullStack",
        database="our_users1"
    )
    print("thius is my given email")
    mycursor = mydb.cursor()
    
    sql = "DELETE FROM affiliate WHERE email = %s"
    val = (givenEmail,)
  
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record(s) deleted")
    return []

 

@auth_blueprint.route('/registerDB/<givenEmail>', methods=['GET', 'POST'])
def registerDB(givenEmail):
    rform = affiliateRegister()
    rform.email.data = givenEmail
    rform.set_department_choices()
    user_to_delete = Affiliate.query.filter_by(email=givenEmail).first()
    finalF =  user_to_delete.firstname
    finalL= user_to_delete.lastname
    rform.firstname.data = finalF
    rform.lastname.data = finalL
    rform.email.render_kw = {'readonly': True}
    print(finalF)
    print(finalL)
    print("GOKU ARE U THERE2")
   # testD(givenEmail)
    # Check if the form was submitted and valid
    if rform.validate_on_submit():
      
        
        user_to_delete = Affiliate.query.filter_by(email=givenEmail).first()
        print(f"user_to_delete: {user_to_delete}")  # Add this line for debugging
        print("GOKU ARE U THERE1")
        if user_to_delete:
            print(f"User found: {user_to_delete.firstname}") 
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Existing user deleted successfully.')

        # Create a new user based on the form information
        new_affiliate = Affiliate(
            email=givenEmail,
            firstname= finalF,
            lastname=user_to_delete.lastname,
            membership= finalL,
            url=rform.url.data,
            # ... other fields you want to set for the new user
        )
        new_affiliate.set_password(password=rform.password.data)
        
        department_name = rform.department.data
        department = Department.query.filter_by(name=department_name).first()
        if department:
            new_affiliate.departments = [department]
            new_affiliate.department = department_name

        if Affiliate.query.count() == 0:
            new_affiliate.is_admin = True

        new_affiliate.is_validated = 1
       # db.session.add(new_affiliate)
      #  db.session.commit()

        flash('New user created successfully.')
        return redirect(url_for('routes.index'))

    return render_template('registerDB.html', form=rform, givenEmail=givenEmail)



########################validate email for existing users

@auth_blueprint.route('/checkEmail', methods=['GET', 'POST'])
def checkEmail():
    all_affiliates = Affiliate.query.all()

    # Extract emails from the affiliates
    all_emails = [affiliate.email for affiliate in all_affiliates if affiliate.email]
    for affiliate in all_affiliates:
        if affiliate.email == "brian.joo@wsu.edu":
            # Print "yes" for found email
            print("yes")
            # Print affiliate information
            print(f"Affiliate ID: {affiliate.id}")
            print(f"First Name: {affiliate.firstname}")
            print(f"Last Name: {affiliate.lastname}")
            # Print other affiliate information as needed
            # You can also return the affiliate information as JSON
           
    return []
   
@auth_blueprint.route('/validateEmail', methods=['GET', 'POST'])
def validateEmail():

    form = EmailForm()  # Creating an instance of the EmailForm class

    if form.validate_on_submit():  # If the form is submitted and validated
        email = form.email.data  # Get the email entered by the user
        return redirect(url_for('auth.email1', givenEmail=email))

    return render_template('email_template.html', form=form)







@auth_blueprint.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        return redirect(url_for('auth.register', givenEmail=email))

    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    
@auth_blueprint.route('/email/<givenEmail>', methods=['GET', 'POST'])
def email1(givenEmail):
    if request.method == 'GET':

        # email = request.form['email']
        print("1")
        email = givenEmail
        print(email)
        token = s.dumps(email, salt='email-confirm')
        print("2")
        msg = Message(
            'Confirm Email', sender='wsuaffiliateconfirmation@outlook.com', recipients=[email])
        print("3")
        link = url_for('auth.confirm_email', token=token,
                       _external=True)  # look at later
        print("this is test\n")
        print(application.config['MAIL_SERVER'])
        print(application.config['MAIL_PORT'])
        msg.body = 'Your link is {}'.format(link)
    # msg.body="test"ws1
    # g@gmail.com

        try:
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", str(e))

       # return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
        return 'email sending...please check email'

    



@auth_blueprint.route('/register/<givenEmail>', methods=['GET', 'POST'])
def register(givenEmail):
    rform = affiliateRegister()
    rform.email.data = givenEmail
    rform.set_department_choices()
    rform.email.render_kw = {'readonly': True}
    is_empty = Affiliate.query.count()
    
    if rform.validate_on_submit():
        # Creating the Affiliate object
        affiliate = Affiliate(
            firstname=rform.firstname.data,
            lastname=rform.lastname.data,
            wsuCampus=rform.wsuCampus.data,
            membership=rform.membership.data,
            
            url=check_url(rform.url.data),
        )
        affiliate.set_password(password=rform.password.data)
        
        department_name = rform.department.data  # Get department name from the form
        department = Department.query.filter_by(name=department_name).first()
        
        if department:
            affiliate.departments = [department]  # Assign the department to the affiliate
            affiliate.department = department_name  # Also assign the name for reference
        
        if is_empty == 0:
            affiliate.is_admin = True
        else:
            affiliate.is_admin = False
        
        db.session.add(affiliate)
        affiliate.email = givenEmail 
        affiliate.is_validated=1
        db.session.commit()
        flash('You are a registered user')
        return redirect(url_for('routes.index'))
    
    return render_template('register.html', form=rform, givenEmail=givenEmail)





@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    lform = LoginForm()

    if lform.validate_on_submit():
        email = lform.email.data

        if not email or email.lower() == 'null':
            flash('Invalid email. Please enter a valid email.')
            return redirect(url_for('auth.login'))

        affiliate = Affiliate.query.filter_by(email=email).first()
        if  affiliate is None:
            flash("That email is not registered. Please sign up")
            return redirect(url_for('auth.login'))
        if affiliate.is_validated == 0:
            flash("You are in the db, but not validated. Please validate user")
            return redirect(url_for('auth.login'))

        elif not affiliate.check_password(lform.password.data):
            flash('Invalid user or password')
            return redirect(url_for('auth.login'))

        elif affiliate.is_ban:
            flash('Your account has been deactivated. Please contact us.')
            return redirect(url_for('routes.index'))

        login_user(affiliate, remember=lform.remember_me.data)
        return redirect(url_for('routes.index'))

    return render_template('login.html', title='Sign in', form=lform)




@auth_blueprint.route('/user', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_admin:
        all_affiliates = Affiliate.query.order_by(Affiliate.firstname).all()
        if request.method == "POST":
            if request.form["submit_button"] == "Deactivate":
                delete_users = request.form.getlist("user_check")
                for user in delete_users:
                    delete_user = Affiliate.query.filter_by(
                        id=int(user)).first()
                    delete_user.is_ban = True
                    db.session.add(delete_user)
                db.session.commit()
                flash("You have successfully deleted users")
                return redirect(url_for("auth.admin"))
        return render_template("admin.html", title="Users", all_affiliates=all_affiliates)
    else:
        flash("You are not authorised")
        return redirect(url_for('routes.index'))


@auth_blueprint.route('/add_interest', methods=['GET', 'POST'])
@login_required
def add_interest():
    if current_user.is_admin:
        form = AddKeywords()
        if form.validate_on_submit():
            print("this went through")
            new_interest = Interest(name=form.name.data)
            db.session.add(new_interest)
            db.session.commit()
            flash('Registered new Keyword')
            return redirect(url_for('auth.tags'))

        return render_template('add_keyword.html', title="Add Interest", form=form)
    else:
        flash("You are not authorised")
        return redirect(url_for("routes.index"))


@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/admin_edit_profile/<user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_profile(user_id):
    if current_user.is_admin:
        user = Affiliate.query.filter_by(id=user_id).first()
        form = AdminEditProfile()
        if form.validate_on_submit():
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.wsuCampus = form.campus.data
            user.department = form.department.data
            user.areaofinterest = form.areaofinterest.data
            user.url = check_url(form.URL.data)
            user.is_admin = form.is_admin.data
            user.is_ban = form.is_ban.data
            db.session.add(user)
            db.session.commit()
            flash("You have edited {first} {last} profile.".format(
                first=user.firstname, last=user.lastname))
            return redirect(url_for('auth.admin'))
        
        elif request.method == 'GET':
            form.firstname.data = user.firstname
            form.lastname.data = user.lastname
            form.campus.data = user.wsuCampus
            if user.departments:
                # Fill the form with the first department's name
                form.department.data = user.departments[0].name
            form.URL.data = user.url
            form.is_ban.data = user.is_ban
            form.is_admin.data = user.is_admin
            
        return render_template('admin_edit_profile.html', form=form, user=user)
    else:
        flash("You are not authorised")
        return redirect(url_for("routes.index"))

@auth_blueprint.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
    if current_user.is_admin:
        interests = Interest.query.order_by(Interest.name).all()
        campuses = Campus.query.order_by(Campus.name).all()
        print(interests)

        if request.method == "POST":
            if request.form["submit_button"] == "Delete":
                delete_interests = request.form.getlist("delete_interests")
                delete_campuses = request.form.getlist("delete_campuses")

                for delete_interest in delete_interests:
                    del_interest = Interest.query.filter_by(
                        id=int(delete_interest)).first()
                    db.session.delete(del_interest)

                for delete_campus in delete_campuses:
                    del_campus = Campus.query.filter_by(
                        id=int(delete_campus)).first()
                    db.session.delete(del_campus)

                db.session.commit()
                flash("You have successfully deleted some tags.")
                return redirect(url_for("auth.tags"))
        return render_template('tags.html', title="Tags", interests=interests, campuses=campuses)
    else:
        flash("You are not authorized")
        return redirect(url_for("routes.index"))


@auth_blueprint.route('/add_campus', methods=['GET', 'POST'])
@login_required
def add_campus():
    if current_user.is_admin:
        form = AddKeywords()
        if form.validate_on_submit():
            campus = Campus(name=form.name.data)
            db.session.add(campus)
            db.session.commit()
            return redirect(url_for('auth.tags'))

        return render_template('add_campus.html', title="Add Campus", form=form)
    else:
        flash("You are not authorized")
        return redirect(url_for("routes.index"))


def check_url(url):
    if "https://" in url or "http://" in url:
        if "https://" in url:
            new_url = url[7:]
            return new_url
        else:
            new_url = url[6:]
            return new_url
    else:
        return url
