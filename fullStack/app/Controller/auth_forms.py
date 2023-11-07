from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Affiliate, Department
from flask_login import current_user


class affiliateRegister(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    wsuCampus = SelectField('Campus', choices=[('Please Select an Option Below'), ('WSU Pullman'), ('WSU Spokane'), (
        'WSU Tri-Cities'), ('WSU Vancouver'), ('WSU Everett'), ("WSU Global Campus")], validators=[DataRequired()])
    department = SelectField('Department', choices=[])
    membership = SelectField('Membership', choices=[(
        'Please Select an Option Below'), ('Yes'), ('No')], validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def set_department_choices(self):
        departments = Department.query.order_by(Department.name).all()
        self.department.choices = [
            (department.name, department.name) for department in departments]

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class AddKeywords(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AdminEditProfile(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    campus = StringField('Campus', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    areaofinterest = StringField('Area of Interest')
    URL = StringField('URL')
    is_admin = BooleanField('Is Admin')
    is_ban = BooleanField('Deactivate Account')
    submit = SubmitField('Submit')


class AddIntrest(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subcategory_id = SelectField('Subcategory', coerce=int)
    submit = SubmitField('Submit')


class AddIntrestOld(FlaskForm):
    name = SelectField('Interest Name', choices=[])
    subcategory_id = SelectField('Subcategory', choices=[])
    submit = SubmitField('Submit')





