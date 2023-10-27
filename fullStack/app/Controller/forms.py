from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectMultipleField, StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Affiliate
from flask_login import current_user


class ProfileForm(FlaskForm):
    areaofinterest = SelectField(
        'Area of Interest', validators=[DataRequired()])
    subcategory = SelectMultipleField('Subcategory')
    combined_interests = StringField('Combined Interests')
    submit = SubmitField('Save')


class EditForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    firstname = StringField('First Name:', validators=[DataRequired()])
    lastname = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    campus = SelectField('Campus:', choices=[('Please Select an Option Below'), ('WSU Pullman'), ('WSU Spokane'), (
        'WSU Tri-Cities'), ('WSU Vancouver'), ('WSU Everett'), ("WSU Global Campus")], validators=[DataRequired()])
    department = SelectField('Department:', choices=[('Please Select an Option Below'), ('Anthropology'), ('Art'), ('Chemistry'), ('Criminal Justice and Criminology'), (
        'Digital Technology and Culture'), ('English'), ('History'), ('Mathematics and Statistics'), ('Physics and Astronomy'), ('Psychology'), ('Sociology')], validators=[DataRequired()])

    URL = StringField('URL:')
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password:', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        affiliates = Affiliate.query.filter_by(email=email.data).all()
        for affiliate in affiliates:
            if (affiliate.id != current_user.id):
                raise ValidationError(
                    'The email is already associated with another account. Please use a different email')


class editTagsForm(FlaskForm):
    areaofinterest = SelectField(
        'Area of Interest:')
    #areaofinterest = SelectField('Area of Interest', coerce=int)
    subcategory = SelectField('Sub-Area of Interest:')
    submit = SubmitField('Submit')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class AddProjectsForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    url = StringField('URL of project', validators=[DataRequired()])
    submit = SubmitField('Submit')

# def get_major():
#     return Major.query.all()

# def get_majorlabel(theMajor):
#     return theMajor.name

# class ClassForm(FlaskForm):
#     coursenum = StringField('Course Number',[Length(min=3, max=3)])
#     title = StringField('Course Title',validators=[DataRequired()])
#     major=QuerySelectField('Majors',query_factory=get_major,get_label=get_majorlabel,allow_blank=False)#query facotry is where the data is coming from
#     submit = SubmitField('Post')
