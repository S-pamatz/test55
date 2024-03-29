from wsgiref.validate import validator
from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from pyparsing import Optional
from wtforms import IntegerField, SelectMultipleField, StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Affiliate, Air, Department, Partners, Sponsor, Universities_Colleges, Water, interestform, smallinterestform
from flask_login import current_user

import datetime

def get__current_year():
    today = datetime.date.today()
    return int(today.strftime("%Y"))

class ProfileForm(FlaskForm):
    areaofinterest = SelectField(
        'Area of Interest', validators=[DataRequired()])
    subcategory = SelectMultipleField('Subcategory')
    combined_interests = StringField('Combined Interests')
    submit = SubmitField('Save')

#

class PasswordChangeForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])

class EditForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    #email = StringField('Email:', validators=[DataRequired()])
    campus = SelectField('Campus', choices=[('Please Select an Option Below'), ('WSU Pullman'), ('WSU Spokane'), (
        'WSU Tri-Cities'), ('WSU Vancouver'), ('WSU Everett'), ("WSU Global Campus")])
    department = SelectField('Department', choices=[])
    university = SelectField('University')
  #  wsu_faculty = SelectField('wsu_faculty', choices=[('Please Select an Option Below'), ('WSU professor'), ('WSU faculty')])
    #sponsor = SelectField('Sponsor')
   # partners = SelectField('Partners')

 #   membership = SelectField('Membership', choices=[(
   #     'Please Select an Option Below'), ('Yes, I am a member'), ('No, I am not a member')])
    URL = StringField('URL')
    password = PasswordField('Password', validators=[])
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password')])
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
    authors = StringField('Authors', validators=[DataRequired()], render_kw={"placeholder": "e.g. 'Bruce Wayne, Mary Jane..."})
    name = StringField('Title of Project', validators=[DataRequired()], render_kw={"placeholder": "e.g. Quaternary Science Reviews"})
    year = SelectField('Years of Operations', choices=[("Present", "Present") if date == get__current_year() else (date,date) for date in range(get__current_year(), 1900, -1) ])
    url = StringField('URL of Project', render_kw={"placeholder": ""})
    partners = SelectField('Partners')
    sponsor = SelectField('Sponsor')
    submit = SubmitField('Submit')
    def set_sponsor(self):

        sponsor = Sponsor.query.order_by(
            Sponsor.id).all()
        self.sponsor.choices = [(uni.name, uni.name)
                                for uni in sponsor]
    def set_partners(self):

        partners = Partners.query.order_by(Partners.id).all()
        self.partners.choices = [(partner.name, partner.name)
                                 for partner in partners]

class AddExperiencesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "e.g. Professor, Teaching Assistant"})
    location = StringField('Institute', render_kw={"placeholder": "e.g. Washington State University"})
    date_from = SelectField('From', choices=[("Present", "Present") if date == get__current_year() else (date,date) for date in range(get__current_year(), 1900, -1) ])
    date_to = SelectField('To', choices=[("Present", "Present") if date == get__current_year() else (date,date) for date in range(get__current_year(), 1900, -1) ])
    submit = SubmitField('Submit')


class AddEducationForm(FlaskForm):
    degree = SelectField("Degree", choices=[("Ph.D.", "Ph.D."), ("M.S.", "M.S."), ("B.S.","B.S.")])
    name = StringField("Name of Degree", validators=[DataRequired()], render_kw={"placeholder": "e.g. Computer Science"})
    year = SelectField('Date of Completion', choices=[("Present", "Present") if date == get__current_year() else (date,date) for date in range(get__current_year(), 1900, -1) ])
    college = StringField("College/University", validators=[], render_kw={"placeholder": "e.g. Washington State University"})
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



class Edit(FlaskForm):
    air = SelectField('Air')
    water = SelectField('Water')

    def set_air_choices(self):
        air_values = Air.query.with_entities(Air.name).all()
        self.air.choices = [(air.name, air.name) for air in air_values]

    def set_water_choices(self):
        water_values = Water.query.with_entities(Water.name).all()
        self.water.choices = [(water.name, water.name) for water in water_values]


class ask(FlaskForm):
    questiom = SelectField('Did you write:', choices=[('Please Select an Option Below'), ('Yes'), ('No')])
    submit = SubmitField('Submit')



class PublicationForm(FlaskForm):
    authors = StringField('Authors', render_kw={"placeholder": "e.g. Boll, J., T. Link, M. Santelmann, R. Heinse, and B. Cosens."})
    title = StringField('Title', render_kw={"placeholder": "e.g. Effects of road construction on soil degradation and nutrient transport in Caspian Hyrcanian mixed forests"})
    journal = StringField('DOI')
 #   volume = IntegerField('Volume', render_kw={"placeholder": "e.g. 11(8)"})
#    issue = IntegerField('Issue', render_kw={"placeholder": "e.g. 63"})
    publication_year = IntegerField('Publication Year', render_kw={"placeholder": "e.g. 2001, 2002"})
  #  page_range = StringField('Page Range', render_kw={"placeholder": "e.g. 0 - 100"})
    submit = SubmitField('Submit')



class EmailForm(FlaskForm):
    email=StringField('Email')
    submit = SubmitField('Submit')



class editPublication(FlaskForm):
    authors = StringField('Authors', render_kw={"placeholder": "e.g. Boll, J., T. Link, M. Santelmann, R. Heinse, and B. Cosens."})
    title = StringField('Title', render_kw={"placeholder": "e.g. Effects of road construction on soil degradation and nutrient transport in Caspian Hyrcanian mixed forests"})
    journal = StringField('Journal', render_kw={"placeholder": "e.g. Nature Communications"})
    volume = IntegerField('Volume', render_kw={"placeholder": "e.g. 11(8)"})
    issue = IntegerField('Issue', render_kw={"placeholder": "e.g. 63"})
    publication_year = IntegerField('Publication Year', render_kw={"placeholder": "e.g. 2001, 2002"})
    page_range = StringField('Page Range', render_kw={"placeholder": "e.g. 0 - 100"})
    submit = SubmitField('Submit')

from wtforms.validators import DataRequired, Optional

class NonValidatingSelectField(SelectField):
    """
    Attempt to make an open-ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate(self, form):
        pass

    def validate(self, form, extra_validators=tuple()):
        # Override the validate method to disable choices validation
        pass
class NonValidatingSelectField1(SelectField):
    """
    Attempt to make an open-ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate(self, form):
        pass

    def validate(self, form, extra_validators=tuple()):
        # Override the validate method to disable choices validation
        pass



class EditInterest(FlaskForm):
    name = SelectField('Interest',  default='', validators=[Optional(None)])
    submit = SubmitField('Submit')

    def set_name(self):
        big_interests = interestform.query.order_by(
            interestform.id).all()

        # Add the choices to the SelectField
        self.name.choices = [(uni.name, uni.name) for uni in big_interests]

class EditInterestSmall(FlaskForm):
    name = SelectField('Sub-Interests', default='', validators=[Optional(None)])
    submit = SubmitField('Submit')

    def set_name_small(self):
        small_interests = smallinterestform.query.order_by(
            smallinterestform.id).all()

        # Add the choices to the SelectField
        self.name.choices = [(uni.name, uni.name) for uni in small_interests]
