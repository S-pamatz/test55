from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db

from app.Controller.auth_forms import LoginForm, affiliateRegister, AddKeywords, AdminEditProfile
from app.Model.models import Affiliate, Interest, Campus
from flask_login import login_user, current_user, logout_user, login_required
from config import Config

auth_blueprint = Blueprint('auth', __name__)
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    rform = affiliateRegister()
    is_empty = Affiliate.query.count()
    if rform.validate_on_submit():
        affiliate = Affiliate(firstname=rform.firstname.data,
                              lastname=rform.lastname.data,
                              wsuCampus=rform.wsuCampus.data,
                              department=rform.department.data,
                              url=check_url(rform.url.data),
                              email=rform.email.data)
        affiliate.set_password(password=rform.password.data)

        if is_empty == 0:
            affiliate.is_admin = True
        else:
            affiliate.is_admin = False

        db.session.add(affiliate)
        db.session.commit()
        flash('You are  a registered user')
        return redirect(url_for('routes.index'))

    return render_template('register.html', form=rform)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    lform = LoginForm()

    if lform.validate_on_submit():
        affiliate = Affiliate.query.filter_by(email=lform.email.data).first()
        if (affiliate is None) or (affiliate.check_password(lform.password.data) == False):  # if login fails
            flash('Invalid user or password')
            return redirect(url_for('auth.login'))

        login_user(affiliate, remember=lform.remember_me.data)
        return redirect(url_for('routes.index'))

    return render_template('login.html', title='Sign in', form=lform)


@auth_blueprint.route('/user', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_admin:
        all_affiliates = Affiliate.query.order_by(Affiliate.firstname).all()
        if request.method == "POST":
            if request.form["submit_button"] == "Delete":
                delete_users = request.form.getlist("user_check")
                for user in delete_users:
                    delete_user = Affiliate.query.filter_by(
                        id=int(user)).first()
                    db.session.delete(delete_user)
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
            db.session.add(user)
            db.session.commit()
            flash("You have edited {first} {last} profile.".format(
                first=user.firstname, last=user.lastname))
            return redirect(url_for('auth.admin'))
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
