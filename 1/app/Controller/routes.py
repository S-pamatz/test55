import base64
import csv
from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db
import pandas as pd
import secrets
import os
from app.Controller.auth_forms import affiliateRegister
from app.Controller.forms import EditForm, AddProjectsForm
from app.Model.models import Affiliate, Project
from flask_login import login_user, current_user, logout_user, login_required
from config import Config

routes_blueprint = Blueprint('routes',__name__)
routes_blueprint.template_folder=Config.TEMPLATE_FOLDER

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(Config.STATIC_FOLDER ,picture_fn)
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
    image_file = url_for('static', filename= current_user.image_file)
    return render_template('display_profile.html',title='Display Profile', affiliate=current_user, image_file=image_file)

@routes_blueprint.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    image_file = url_for('static', filename= current_user.image_file)
    eform=EditForm()
    if request.method == 'POST':
        #handle the form submission
        if eform.validate_on_submit():

            if eform.picture.data:
                picture_file = save_picture(eform.picture.data)
                current_user.image_file = picture_file
                
            current_user.firstname= eform.firstname.data
            current_user.lastname=  eform.lastname.data
            current_user.email=  eform.email.data
            current_user.wsuCampus= eform.campus.data
            current_user.department= eform.department.data
            current_user.areaofinterest= eform.areaofinterest.data
            current_user.url= eform.URL.data

            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your changes have been saved')
            return redirect(url_for('routes.index'))  

        pass
    elif request.method=='GET':
        #populate the user data from the DB
        eform.firstname.data=current_user.firstname
        eform.lastname.data=current_user.lastname
        eform.email.data=current_user.email
        eform.campus.data = current_user.wsuCampus
        eform.department.data = current_user.department
        eform.areaofinterest.data = current_user.areaofinterest
        eform.URL.data = current_user.url
       
    else: 
        pass

    return render_template('edit_profile.html',title='Edit Profile',form=eform, image_file=image_file)


@routes_blueprint.route('/add_projects', methods=["POST", "GET"])
@login_required
def add_projects():
    afform = AddProjectsForm()

    if afform.validate_on_submit():
        project = Project(name=afform.name.data, url=check_url(afform.url.data))
        current_user.projects.append(project)
        db.session.add(project)
        db.session.commit()
        flash("You have added {project_name}".format(project_name=project.name))
        return redirect(url_for('routes.index'))
    
    return render_template('add_projects.html', title='Add project', form=afform)

@routes_blueprint.route('/displayAllUsers', methods=['GET', 'POST'])
def displayAll():
    print("test")

    users = Affiliate.query.all()
    image_urls = []

    # Loop through the users and generate image URLs
    for user in users:
        image_file = url_for('static', filename=user.image_file)
        image_urls.append(image_file)

    # Combine users and image_urls into a list of tuples
    user_data = zip(users, image_urls)

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
    
@routes_blueprint.route('/readFile',methods=['GET','POST'])
def read():
    df = pd.read_csv("db.csv", usecols = ['Email'])  
    if request.method == 'GET':
        return '<form action="/readFile" method="POST"><input name="email"><input type="submit"></form>'
    email = request.form['email']
    if(readFile(email)==True):
        flash("this email is in our db. we will re-route you to the validation page")
        return redirect(url_for('routes.tData',givenEmail=email)) 
    else:
        flash("this email is not in our db. we will redirect you to the register page")
        return redirect(url_for('auth.register'))  


def readFile(email):
    df = pd.read_csv("db.csv", usecols = ['Email', 'Name', 'Department'])
    print(type(df))
    if email in df['Email'].values:
        return True
    else:
        return False
    
def getMail(email):
    listInfo=[]
    df = pd.read_csv("db.csv", usecols = ['Email', 'Name', 'Department','URL','WSU Campus'])


    if email in df['Email'].values:
            # Access 'Name' and 'Department' values based on the condition
            name = df[df['Email'] == email]['Name'].values[0]
            department = df[df['Email'] == email]['Department'].values[0]
            url=df[df['Email'] == email]['URL'].values[0]

            campus=df[df['Email'] == email]['WSU Campus'].values[0]
            print(f"Name: {name}")
            fullName=name.split(" ")
            print(f"Department: {department}")
            print(f"url: {url}")
      #  print(f"URL: {url}")
            listInfo.append(email)#index 0
            listInfo.append(fullName[0])#first#index 1
            listInfo.append(fullName[1])#last#index 2

            listInfo.append(campus)#index 3
            listInfo.append(url)#index 4
            listInfo.append(department)

    return listInfo

@routes_blueprint.route('/tData/<givenEmail>',methods=['GET','POST'])
def tData(givenEmail):
    rform=affiliateRegister()
    list1=getMail(givenEmail)

    rform.email.default = list1[0]
    rform.firstname.default= list1[1]
    rform.lastname.default= list1[2]
    rform.wsuCampus.default= list1[3]
    rform.url.default=list1[4]
    rform.department.default= list1[5]
    rform.process()
    print(list1)
    print("this is the given email ",givenEmail)
    if rform.validate_on_submit():
        affiliate=Affiliate(firstname=rform.firstname.data,
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

    return render_template('register.html',form=rform,emailTest=list1[0])

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