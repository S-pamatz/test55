from datetime import datetime
from flask import render_template, flash, redirect, url_for, request,Blueprint
from app import db

from app.Controller.auth_forms import LoginForm, RegistrationForm,affiliateRegister
from app.Model.models import Class, Major, Student,Affiliate
from flask_login import login_user,current_user,logout_user,login_required
from config import Config

auth_blueprint = Blueprint('auth',__name__)
auth_blueprint.template_folder=Config.TEMPLATE_FOLDER


@auth_blueprint.route('/register/',methods=['GET','POST'])
def register():
    rform=affiliateRegister()

    if rform.validate_on_submit():
        affiliate=Affiliate(name=rform.name.data,
        wsuCampus=rform.wsuCampus.data,
        department=rform.department.data,
        url=rform.url.data,
        email=rform.email.data)
        affiliate.set_password(rform.password.data)

        db.session.add(affiliate)
        db.session.commit()
        flash('You are  a registered user')
        return redirect(url_for('routes.index2')) 

    return render_template('register.html',form=rform)



@auth_blueprint.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index')) 
    lform=LoginForm()

    if lform.validate_on_submit():
        affiliate=Affiliate.query.filter_by(name=lform.name.data).first()
        if (affiliate is None) or (affiliate.check_password(lform.password.data)==False):#if login fails
            flash('Invalid user or password')
            return redirect(url_for('auth.login'))

        login_user(affiliate,remember=lform.remember_me.data)
        return redirect(url_for('routes.index2'))  

    return render_template('login.html',title='Sign in',form=lform)


@auth_blueprint.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
