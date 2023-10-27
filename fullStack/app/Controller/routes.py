from flask import Flask, jsonify
import base64
import csv
from flask import make_response, render_template, flash, redirect, url_for, request, Blueprint, jsonify
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from app import db
import pandas as pd
import secrets
import os
import app
from app.Controller.auth_forms import AddIntrest, AddIntrestOld, AddKeywords, affiliateRegister
from app.Controller.forms import EditForm, AddProjectsForm, editTagsForm
from app.Model.models import Affiliate, Interest, IntrestTest, Project, Subcategory
from flask_login import login_user, current_user, logout_user, login_required
from config import Config
from flask import Flask
from flask_mail import Mail, Message
routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER


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


@routes_blueprint.route('/email/<givenEmail>', methods=['GET', 'POST'])
def email(givenEmail):
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
        link = url_for('routes.confirm_email', token=token,
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


@routes_blueprint.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

    return redirect(url_for('routes.tData', givenEmail=email))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(Config.STATIC_FOLDER, picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@routes_blueprint.route('/home', methods=['GET'])
def tempIndex():
    return render_template('cereoLink.html')


@routes_blueprint.route('/index', methods=['GET'])
@routes_blueprint.route('/', methods=['GET'])
@login_required
def index():
    #eform = EmptyForm()
    image_file = url_for('static', filename=current_user.image_file)
    return render_template('display_profile.html', title='Display Profile', affiliate=current_user, image_file=image_file)


@routes_blueprint.route('/get_subcategories/<int:interest_id>')
def get_subcategories(interest_id):
    interest = IntrestTest.query.get(interest_id)

    if interest is not None:
        interests_with_same_name = IntrestTest.query.filter_by(
            name=interest.name).all()
        subcategory_options = ""

        for i in interests_with_same_name:
            subcategories = i.subcategory
            if subcategories:
                if not isinstance(subcategories, list):
                    subcategories = [subcategories]

                for subcategory in subcategories:
                    subcategory_options += f"<option value='{subcategory.id}'>{subcategory.name}</option>"

        return subcategory_options

    return "No subcategories found for this interest."


@routes_blueprint.route('/test_saved_tags', methods=['GET'])
def test_saved_tags():
    user_interests = current_user.interests
    combined_data = {}

    for interest in user_interests:
        interest_name = interest.name
        subcategory_name = interest.subcategory.name if interest.subcategory else None

        if interest_name not in combined_data:
            combined_data[interest_name] = {
                "Interest": interest_name, "SubCategories": []}

        if subcategory_name:
            combined_data[interest_name]["SubCategories"].append(
                subcategory_name)

    result_data = list(combined_data.values())

    return jsonify({
        current_user.email: result_data
    })


@routes_blueprint.route('/addTags', methods=['GET', 'POST'])
@login_required
def addTags():
    interests = IntrestTest.query.order_by(IntrestTest.name).all()
    subcategories = Subcategory.query.all()
    print("1")
    eform = editTagsForm()
    print("2")
    # Populate the area of interest choices
    eform.areaofinterest.choices = [
        (interest.id, interest.name) for interest in interests]
    print("3")
    # Populate the subcategory choices
    eform.subcategory.choices = [(subcategory.id, subcategory.name)
                                 for subcategory in subcategories]
    print("4")
    if request.method == 'POST':
        if eform.validate_on_submit():
            selected_interest = IntrestTest.query.get(
                eform.areaofinterest.data)

            # Update the user's interests
            current_user.interests.append(selected_interest)

            # Now, you can access the subcategory through the selected_interest
            selected_subcategory = selected_interest.subcategory

            db.session.commit()
            flash('Your changes have been saved')
            return redirect(url_for('routes.addTags'))

    elif request.method == 'GET':
        print("5")
        eform.areaofinterest.data = current_user.interests
    print("8")
    return render_template('addTags.html', title='addTags', form=eform, interests=interests, subcategories=subcategories)


@routes_blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    image_file = url_for('static', filename=current_user.image_file)
    eform = EditForm()
    if request.method == 'POST':
        # handle the form submission
        if eform.validate_on_submit():

            if eform.picture.data:
                picture_file = save_picture(eform.picture.data)
                current_user.image_file = picture_file

            current_user.firstname = eform.firstname.data
            current_user.lastname = eform.lastname.data
            current_user.email = eform.email.data
            current_user.wsuCampus = eform.campus.data
            current_user.department = eform.department.data

            current_user.url = eform.URL.data

            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your changes have been saved')
            return redirect(url_for('routes.index'))

        pass
    elif request.method == 'GET':
        # populate the user data from the DB
        eform.firstname.data = current_user.firstname
        eform.lastname.data = current_user.lastname
        eform.email.data = current_user.email
        eform.campus.data = current_user.wsuCampus
        eform.department.data = current_user.department

        eform.URL.data = current_user.url

    else:
        pass

    return render_template('edit_profile.html', title='Edit Profile', form=eform, image_file=image_file)


@routes_blueprint.route('/add_projects', methods=["POST", "GET"])
@login_required
def add_projects():
    afform = AddProjectsForm()

    if afform.validate_on_submit():
        project = Project(name=afform.name.data,
                          url=check_url(afform.url.data))
        current_user.projects.append(project)
        db.session.add(project)
        db.session.commit()
        flash("You have added {project_name}".format(
            project_name=project.name))
        return redirect(url_for('routes.index'))

    return render_template('add_projects.html', title='Add project', form=afform)


@routes_blueprint.route('/displayAllUsers', methods=['GET', 'POST'])
def displayAll():
    # print("test")

    # users = Affiliate.query.all()
    # image_urls = []

    # # Loop through the users and generate image URLs
    # for user in users:
    #     image_file = url_for('static', filename=user.image_file)
    #     image_urls.append(image_file)

    # # Combine users and image_urls into a list of tuples
    # user_data = zip(users, image_urls)
    user_data = []

    return render_template('displayAll.html', user_data=user_data)


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


@routes_blueprint.route('/readFile', methods=['GET', 'POST'])
def read():
    df = pd.read_csv("db.csv", usecols=['Email'])
    if request.method == 'GET':
        return '<form action="/readFile" method="POST"><input name="email"><input type="submit"></form>'
    email = request.form['email']
    if (readFile(email) == True):
        flash("this email is in our db. we will re-route you to the validation page")
        return redirect(url_for('routes.email', givenEmail=email))
        # return redirect(url_for('routes.tData', givenEmail=email))
    else:
        flash("this email is not in our db. we will redirect you to the register page")
        return redirect(url_for('auth.register'))


def readFile(email):
    df = pd.read_csv("db.csv", usecols=['Email', 'Name', 'Department'])
    print(type(df))
    if email in df['Email'].values:
        return True
    else:
        return False


def getMail(email):
    listInfo = []
    df = pd.read_csv("db.csv", usecols=[
                     'Email', 'Name', 'Department', 'URL', 'WSU Campus'])

    if email in df['Email'].values:
        # Access 'Name' and 'Department' values based on the condition
        name = df[df['Email'] == email]['Name'].values[0]
        department = df[df['Email'] == email]['Department'].values[0]
        url = df[df['Email'] == email]['URL'].values[0]

        campus = df[df['Email'] == email]['WSU Campus'].values[0]
        print(f"Name: {name}")
        fullName = name.split(" ")
        print(f"Department: {department}")
        print(f"url: {url}")
  #  print(f"URL: {url}")
        listInfo.append(email)  # index 0
        listInfo.append(fullName[0])  # first#index 1
        listInfo.append(fullName[1])  # last#index 2

        listInfo.append(campus)  # index 3
        listInfo.append(url)  # index 4
        listInfo.append(department)

    return listInfo


@routes_blueprint.route('/tData/<givenEmail>', methods=['GET', 'POST'])
def tData(givenEmail):
    rform = affiliateRegister()
    list1 = getMail(givenEmail)

    rform.email.default = list1[0]
    rform.firstname.default = list1[1]
    rform.lastname.default = list1[2]
    rform.wsuCampus.default = list1[3]
    rform.url.default = list1[4]
    rform.department.default = list1[5]
    rform.process()
    print(list1)
    print("this is the given email ", givenEmail)
    if rform.validate_on_submit():
        affiliate = Affiliate(firstname=rform.firstname.data,
                              lastname=rform.lastname.data,
                              wsuCampus=rform.wsuCampus.data,
                              department=rform.department.data,
                              url=rform.url.data,
                              email=list1[0])
        affiliate.set_password(rform.password.data)

        db.session.add(affiliate)
        db.session.commit()
        flash('You are  a registered user')
  #  return redirect(url_for('routes.index'))

    return render_template('register.html', form=rform, emailTest=list1[0])


@routes_blueprint.route('/jsnDerulo', methods=['GET'])
def jsonD():
    jsonData = []

    affiliates = Affiliate.query.all()
    for user in affiliates:
       # print(user.email)
        jsonData.append({
            "firstName": user.firstname,
            "lastName": user.lastname,
            "wsu campus": user.wsuCampus,
            "department": user.department,
            "email": user.email
        })
    # Convert the data to a JSON string
    json_data = jsonify(jsonData)

    # Create a Response with the JSON data and set headers for download
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=affiliates.json"
    response.headers["Content-Type"] = "application/json"

    return response

@routes_blueprint.route('/search', methods=['GET'])
def search():
    inputValue = request.args.get("inputValue")

    # Search through the relevant fields for the inputValue
    affiliates = db.session.query(Affiliate).filter(
        Affiliate.firstname.ilike(f"%{inputValue}%") |
        Affiliate.lastname.ilike(f"%{inputValue}%") |
        Affiliate.wsuCampus.ilike(f"%{inputValue}%") |
        Affiliate.department.ilike(f"%{inputValue}%") |
        Affiliate.email.ilike(f"%{inputValue}%") |
        Affiliate.url.ilike(f"%{inputValue}%")
    ).all()

    # Construct the response data
    response_data = []
    for affiliate in affiliates:
        response_data.append({
            "Interest": '',
            "Department": getattr(affiliate, 'department', ''),
            "Name": f"{getattr(affiliate, 'firstname', '')} {getattr(affiliate, 'lastname', '')}".strip(),
            "Membership": '',  # placeholder, adjust as needed
            "WSUCampus": getattr(affiliate, 'wsuCampus', ''),
            "Email": getattr(affiliate, 'email', ''),
            "URL": getattr(affiliate, 'url', '')
        })

    return jsonify(response_data)


@routes_blueprint.route('/jsnKey', methods=['GET'])
def jsonK():
    print("sd")
    jsonDey = []

    intrests = Interest.query.all()

    for i in intrests:
       # print(user.email)
        jsonDey.append({
            "intrest": i.name,

        })
    # Convert the data to a JSON string
    json_data = jsonify(jsonDey)

    # Create a Response with the JSON data and set headers for download
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=affiliates.json"
    response.headers["Content-Type"] = "application/json"

    return response

    # You can now use the 'keywords' list to process all the entered keywords.


@routes_blueprint.route('/tagTest', methods=['GET'])
def tagTest():
    jsonData = []

    tags = Interest.query.all()
    for tag in tags:
        print(tag)
       # print(user.email)

    return jsonData

# this is just to create big instances

# initial;


@routes_blueprint.route('/createIntrests', methods=['GET', 'POST'])
def createIntrests():
    eForm = AddIntrest()
    eForm.subcategory_id.choices = [
        (subcategory.id, subcategory.name) for subcategory in Subcategory.query.all()]

    if eForm.validate_on_submit():
        interest = IntrestTest(
            name=eForm.name.data,
            subcategory_id=eForm.subcategory_id.data
        )
        db.session.add(interest)
        db.session.commit()

        # Add a success message
        flash("Interest added successfully", "success")
        # Redirect back to the form page
        return redirect(url_for('routes.createIntrests'))

    return render_template('createIntrests.html', form=eForm)


@routes_blueprint.route('/createIntrestsRepeat', methods=['GET', 'POST'])
def createIntrestsRepeat():
    eForm = AddIntrestOld()

    # Fetch unique interest names from your database
    unique_interest_names = list(
        set(interest.name for interest in IntrestTest.query.all()))

    # Fetch unique subcategory names from your database
    unique_subcategory_names = list(
        set(subcategory.name for subcategory in Subcategory.query.all()))

    # Populate the dropdowns with unique interest and subcategory names
    eForm.name.choices = [(name, name) for name in unique_interest_names]
    eForm.subcategory_id.choices = [(name, name)
                                    for name in unique_subcategory_names]

    if eForm.validate_on_submit():
        # Get the selected values from the form
        selected_interest_name = eForm.name.data
        selected_subcategory_name = eForm.subcategory_id.data

        # Find the corresponding interest and subcategory records based on their names
        interest = IntrestTest.query.filter_by(
            name=selected_interest_name).first()
        subcategory = Subcategory.query.filter_by(
            name=selected_subcategory_name).first()

        # Create a new IntrestTest record with the selected interest and subcategory
        new_interest = IntrestTest(
            name=interest.name,
            subcategory=subcategory
        )

        db.session.add(new_interest)
        db.session.commit()

        # Add a success message
        flash("Interest added successfully", "success")
        # Redirect back to the form page
        return redirect(url_for('routes.createIntrestsRepeat'))

    return render_template('createIntrestsRepeat.html', form=eForm)


@routes_blueprint.route('/displayAllIntrests', methods=['GET', 'POST'])
def displayIntrests():
    interests = IntrestTest.query.order_by(IntrestTest.name).all()
    return render_template('displayIntrestsAll.html', title="Tags", interests=interests)


@routes_blueprint.route('/displaySubCategory', methods=['GET', 'POST'])
def displayDub():
    interests = IntrestTest.query.order_by(IntrestTest.name).all()
    return render_template('displaySub.html', title="Interests", interests=interests)


@routes_blueprint.route('/interests_json', methods=['GET'])
def interests_json():
    data = []

    interests = IntrestTest.query.order_by(IntrestTest.name).all()

    for interest in interests:
        interest_data = {
            "Interest": interest.name,
            "Subcategory": None
        }

        if interest.subcategory:
            interest_data["Subcategory"] = interest.subcategory.name

        data.append(interest_data)

    # Convert the data to a JSON response
    json_data = jsonify(data)

    # Create a Response with the JSON data and set headers for download
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=affiliates.json"
    response.headers["Content-Type"] = "application/json"

    return response


@routes_blueprint.route('/testSub', methods=['GET'])
def testSub():

    data = []

    # Assuming you have a makeDictFromIntrests function
    interest_dict = makeDictFromIntrests()

    # Convert the dictionary to a list of dictionaries
    for interest, subcategories in interest_dict.items():
        data.append({
            "Interest": interest,
            "Subcategories": subcategories
        })

    # Convert the data to a JSON response
    json_data = jsonify(data)

    # Create a Response with the JSON data
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=intrests.json"
    response.headers["Content-Type"] = "application/json"
    return response


def makeDictFromIntrests():

    dict1 = {}
    t = 1
    interests = IntrestTest.query.order_by(IntrestTest.name).all()
    for interest in interests:
        if interest.name in dict1:
            dict1[interest.name].append(interest.subcategory.name)
        else:
            dict1[interest.name] = [
                interest.subcategory.name] if interest.subcategory else []

    return dict1


# @routes_blueprint.route('/', methods=['GET'])#/=root pathx
# @routes_blueprint.route('/index', methods=['GET'])
# @login_required
# def index():
#     #eform = EmptyForm()
#     #retrieve all classes in the data base
#     allclasses= Class.query.order_by(Class.major).all()#this is sorting by major

#     return render_template('index.html', title="Course List",classes=allclasses)#to display all the classes, i need to put in in the parameters
#                                                         #the second classes is the classes on line 15
#                                                         #the first classes is the argument name that we pass through to render the template
#                                                         #and it will be available when we render the index.html

# @routes_blueprint.route('/createclass/',methods=['GET','POST'])
# @login_required
# def createclass():
#     cform = ClassForm()
#     if cform.validate_on_submit():
#         newClass=Class(coursenum=cform.coursenum.data,title=cform.title.data,major=cform.major.data.name,)#since major is a drop down we need to get the name from the data
#         db.session.add(newClass)
#         db.session.commit()
#         flash('Class "'+newClass.major+'-'+newClass.coursenum+'" is created')
#         return redirect(url_for('routes.index'))
#     return render_template('create_class.html', form=cform)

# @routes_blueprint.route('/display_profile',methods=['GET'])
# @login_required
# def display_profile():
#     #eform=EmptyForm()
#     return render_template('display_profile.html',title='Display Profile',student=current_user)

# @routes_blueprint.route('/roster/<classid>',methods=['GET'])#we will include the class id in the path
# @login_required
# def roster(classid):
#     theclass=Class.query.filter_by(id=classid).first()
#     return render_template('roster.html',title="Class Roster",current_class=theclass)

# @routes_blueprint.route('/enroll/<classid>',methods=['POST'])
# @login_required
# def enroll(classid):
#     #eform=EmptyForm()
#     #if eform.validate_on_submit():
#     theclass=Class.query.filter_by(id=classid).first()
#     if theclass is None:
#         flash('Class with id "{}" not found '.format(classid))
#         return redirect(url_for('routes.index'))
#     current_user.enroll(theclass)
#     db.session.commit()
#     flash('You are now enrolled in class {} {}!'.format(theclass.major,theclass.coursenum))
#     return redirect(url_for('routes.index'))
#     #else:
#       #  return redirect(url_for('index'))

# @routes_blueprint.route('/unenroll/<classid>',methods=['POST'])
# @login_required
# def unenroll(classid):
#     #eform=EmptyForm()
#     #if eform.validate_on_submit():
#     theclass=Class.query.filter_by(id=classid).first()
#     if theclass is None:
#         flash('Class with id "{}" not found '.format(classid))
#         return redirect(url_for('routes.index'))
#     current_user.unenroll(theclass)
#     db.session.commit()
#     flash('You are now un-enrolled in class {} {}!'.format(theclass.major,theclass.coursenum))
#     return redirect(url_for('routes.index'))
#    # else:
#       #  return redirect(url_for('index'))

# @routes_blueprint.route('/jsnDerulo', methods=['GET'])
# def jsonD():
 #   jsonData = []

  #  affiliates = Affiliate.query.all()
   # for user in affiliates:
    #   # print(user.email)
    #   jsonData.append({
    #      "firstName": user.firstname,
    #     "lastName": user.lastname,
    #    "wsu campus": user.wsuCampus,
    #   "department": user.department,
    #  "email": user.email
    # })
    # Convert the data to a JSON string
    #json_data = jsonify(jsonData)

    # Create a Response with the JSON data and set headers for download
    #response = make_response(json_data)
    #response.headers["Content-Disposition"] = "attachment; filename=affiliates.json"
    #response.headers["Content-Type"] = "application/json"

    # return response
