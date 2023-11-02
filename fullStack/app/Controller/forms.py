from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectMultipleField, StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Affiliate, Department, Partners, Sponsor, Universities_Colleges
from flask_login import current_user


class ProfileForm(FlaskForm):
    areaofinterest = SelectField(
        'Area of Interest', validators=[DataRequired()])
    subcategory = SelectMultipleField('Subcategory')
    combined_interests = StringField('Combined Interests')
    submit = SubmitField('Save')

#


class EditForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    firstname = StringField('First Name:')
    lastname = StringField('Last Name:')
    #email = StringField('Email:', validators=[DataRequired()])
    campus = SelectField('Campus:', choices=[('Please Select an Option Below'), ('WSU Pullman'), ('WSU Spokane'), (
        'WSU Tri-Cities'), ('WSU Vancouver'), ('WSU Everett'), ("WSU Global Campus")])
    department = SelectField('Department:', choices=[])
    university = SelectField('University:')
    sponsor = SelectField('sponsor:')
    partners = SelectField('partners:')

    membership = SelectField('membership:', choices=[(
        'Please Select an Option Below'), ('Yes, I am a member'), ('No, I am not a member')])
    URL = StringField('URL:')
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password:', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def set_sponsor(self):

        sponsor = Sponsor.query.order_by(
            Sponsor.id).all()
        self.sponsor.choices = [(uni.name, uni.name)
                                for uni in sponsor]
    def set_department_choices(self):
        departments = Department.query.order_by(Department.name).all()
        self.department.choices = [
            (department.name, department.name) for department in departments]
    def set_partners(self):

        partners = Partners.query.order_by(Partners.id).all()
        self.partners.choices = [(partner.name, partner.name)
                                 for partner in partners]

    def set_university_choices(self):

        universities = Universities_Colleges.query.order_by(
            Universities_Colleges.id).all()
        self.university.choices = [(uni.name, uni.name)
                                   for uni in universities]



    def validate_email(self, email):
        affiliates = Affiliate.query.filter_by(email=email.data).all()
        for affiliate in affiliates:
            if (affiliate.id != current_user.id):
                raise ValidationError(
                    'The email is already associated with another account. Please use a different email')


class editTagsForm(FlaskForm):
    areaofinterest = SelectField(
        'Area of Interest:')
  #  areaofinterest = SelectField('Area of Interest', coerce=int, validate_choice=True)
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
