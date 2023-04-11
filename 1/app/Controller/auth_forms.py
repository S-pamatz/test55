from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , TextAreaField, PasswordField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Class, Major, Student, Affiliate
from flask_login import current_user

class affiliateRegister(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    wsuCampus=StringField('wsuCampus',validators=[DataRequired()])
    department=StringField('department',validators=[DataRequired()])
    url=StringField('url',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Repeat password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Register')


  

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    firstname=StringField('First name',validators=[DataRequired()])
    lastname=StringField('last name',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired(),Email()])
    address=TextAreaField('Address',[Length(min=0,max=200)])
    password=PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Repeat password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Register')
    
    def validate_username(self,username):
        student = Student.query.filter_by(username=username.data).first()
        if student is not None:
            raise ValidationError('The user name already exists. Please choose another one ')

    def validate_email(self,email):
        student = Student.query.filter_by(email=email.data).first()
        if student is not None:
            raise ValidationError('The email already exists. Please choose another one ')


class LoginForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    password=StringField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remeber me')
    submit = SubmitField('Sign in')
