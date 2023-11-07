from datetime import datetime
from app import db, login
from enum import unique
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from wtforms.validators import DataRequired


@login.user_loader
def load_user(id):
    return Affiliate.query.get(int(id))
    # return Student.query.filter_by(id=id)


works = db.Table(
    "works",
    db.Column("affiliate_id", db.Integer, db.ForeignKey("affiliate.id")),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id")),
)
interests = db.Table(
    "interests",
    db.Column("affiliate_id", db.Integer, db.ForeignKey("affiliate.id")),
    db.Column("intresttest_id", db.Integer, db.ForeignKey("intrest_test.id")),
)
works_departments = db.Table(
    "works_departments",
    db.Column("affiliate_id", db.Integer, db.ForeignKey("affiliate.id")),
    db.Column("department_id", db.Integer, db.ForeignKey("department.id"))
)
# model is how it is stored in the db. ewach class has certain data that is stored
# forms is what the user sees. it is connected to html

edu = db.Table(
    "edu",
    db.Column("affiliate_id", db.Integer, db.ForeignKey("affiliate.id")),
    db.Column("education_id", db.Integer, db.ForeignKey("education.id"))
)
exp = db.Table(
    "exp",
    db.Column("affiliate_id", db.Integer, db.ForeignKey("affiliate.id")),
    db.Column("experience_id", db.Integer, db.ForeignKey("experience.id"))
)

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class IntrestTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    subcategory = db.relationship('Subcategory', foreign_keys=[
                                  subcategory_id], backref='interests')

class Affiliate(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='Default_pic.png')
    email = db.Column(db.String(120), unique=True, nullable=False, default=None)
    password_hash = db.Column(db.String(128), nullable=False, default=None)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    sponsor = db.Column(db.String(128))
    is_ban = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_validated = db.Column(db.Boolean, default=False)  # New column
    membership = db.Column(db.String(128))
    wsuCampus = db.Column(db.String(128))
    departments = db.relationship(
        "Department", secondary=works_departments, backref="affiliates"
    )
    department = db.Column(db.String(128))  # Single department
    university = db.Column(db.String(128))
    partners = db.Column(db.String(128))
    url = db.Column(db.String(128))
    projects = db.relationship("Project", secondary=works, backref="authors")
    interests = db.relationship("IntrestTest", secondary=interests, backref="affiliates")
    education = db.relationship("Education", secondary=edu, backref="prof")
    experience = db.relationship("Experience", secondary=exp, backref="employee")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    authorss = db.Column(db.String(120))
    year = db.Column(db.Date)
    publisher = db.Column(db.String(120))
    url = db.Column(db.String(120))

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    degree = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Date)
    college = db.Column(db.String(120), nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Universities_Colleges(db.Model):
    __tablename__ = 'universities_colleges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Sponsor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Partners(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

  


class Publication(db.Model):
    __tablename__ = 'publications'

    id = db.Column(db.Integer, primary_key=True)
    authors = db.Column(db.String(255))
    title = db.Column(db.String(255))
    journal = db.Column(db.String(100))
    volume = db.Column(db.Integer)
    issue = db.Column(db.Integer)
    publication_year = db.Column(db.Integer)
    page_range = db.Column(db.String(20))
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliate.id'), nullable=False)
    affiliate = db.relationship('Affiliate', backref=db.backref('publications', lazy=True))

# i think i want to hit something rn

class Air(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Water(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))