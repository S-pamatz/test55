
from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db

from app.Controller.forms import ClassForm, EditForm
from app.Model.models import Class
from flask_login import login_user,current_user,logout_user,login_required
from config import Config

routes_blueprint = Blueprint('routes',__name__)
routes_blueprint.template_folder=Config.TEMPLATE_FOLDER

@routes_blueprint.route('/', methods=['GET'])#/=root pathx
@routes_blueprint.route('/index', methods=['GET'])
@login_required
def index():
    #eform = EmptyForm()
    #retrieve all classes in the data base
    allclasses= Class.query.order_by(Class.major).all()#this is sorting by major

    return render_template('index.html', title="Course List",classes=allclasses)#to display all the classes, i need to put in in the parameters
                                                        #the second classes is the classes on line 15
                                                        #the first classes is the argument name that we pass through to render the template
                                                        #and it will be available when we render the index.html


@routes_blueprint.route('/index2', methods=['GET'])
@login_required
def index2():
    #eform = EmptyForm()
   return render_template('display_profile.html',title='Display Profile',afiliate=current_user)

@routes_blueprint.route('/createclass/',methods=['GET','POST'])
@login_required
def createclass():
    cform = ClassForm()
    if cform.validate_on_submit():
        newClass=Class(coursenum=cform.coursenum.data,title=cform.title.data,major=cform.major.data.name,)#since major is a drop down we need to get the name from the data
        db.session.add(newClass)
        db.session.commit()
        flash('Class "'+newClass.major+'-'+newClass.coursenum+'" is created')
        return redirect(url_for('routes.index')) 
    return render_template('create_class.html', form=cform)



@routes_blueprint.route('/display_profile',methods=['GET'])
@login_required
def display_profile():
    #eform=EmptyForm()
    return render_template('display_profile.html',title='Display Profile',student=current_user)



@routes_blueprint.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():

    eform=EditForm()
    if request.method == 'POST':
        #handle the form submission
        if eform.validate_on_submit():
            current_user.firstname= eform.firstname.data
            current_user.lastname=  eform.lastname.data
            current_user.address=  eform.address.data
            current_user.email=  eform.email.data
            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash('Your changes have been saved')
            return redirect(url_for('routes.display_profile'))  

        pass
    elif request.method=='GET':
        #populate the user data from the DB
        eform.firstname.data=current_user.firstname
        eform.lastname.data=current_user.lastname
        eform.address.data=current_user.address
        eform.email.data=current_user.email
       

    else: 
        pass

    return render_template('edit_profile.html',title='Edit Profile',form=eform)


@routes_blueprint.route('/roster/<classid>',methods=['GET'])#we will include the class id in the path
@login_required
def roster(classid):
    theclass=Class.query.filter_by(id=classid).first()
    return render_template('roster.html',title="Class Roster",current_class=theclass)

@routes_blueprint.route('/enroll/<classid>',methods=['POST'])
@login_required
def enroll(classid):
    #eform=EmptyForm()
    #if eform.validate_on_submit():
    theclass=Class.query.filter_by(id=classid).first()
    if theclass is None:
        flash('Class with id "{}" not found '.format(classid))
        return redirect(url_for('routes.index'))
    current_user.enroll(theclass)
    db.session.commit()
    flash('You are now enrolled in class {} {}!'.format(theclass.major,theclass.coursenum))
    return redirect(url_for('routes.index'))
    #else:
      #  return redirect(url_for('index'))




@routes_blueprint.route('/unenroll/<classid>',methods=['POST'])
@login_required
def unenroll(classid):
    #eform=EmptyForm()
    #if eform.validate_on_submit():
    theclass=Class.query.filter_by(id=classid).first()
    if theclass is None:
        flash('Class with id "{}" not found '.format(classid))
        return redirect(url_for('routes.index'))
    current_user.unenroll(theclass)
    db.session.commit()
    flash('You are now un-enrolled in class {} {}!'.format(theclass.major,theclass.coursenum))
    return redirect(url_for('routes.index'))
   # else:
      #  return redirect(url_for('index'))