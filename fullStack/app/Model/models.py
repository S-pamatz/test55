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

# model is how it is stored in the db. ewach class has certain data that is stored
# forms is what the user sees. it is connected to html



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
    image_file = db.Column(db.String(20), nullable=False,
                           default='Default_pic.png')
    email = db.Column(db.String(120), unique=True,
                      nullable=False, default=None)
    password_hash = db.Column(db.String(128), nullable=False, default=None)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    sponsor = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    membership = db.Column(db.String(128))
    wsuCampus = db.Column(db.String(128))
    #department = db.Column(db.String)
   
    # For heavens sake please don't remove this.
    department = db.Column(db.String(128))
    university = db.Column(db.String(128))
    partners = db.Column(db.String(128))
    url = db.Column(db.String(128))
    projects = db.relationship("Project", secondary=works, backref="authors")
    interests = db.relationship(
        "IntrestTest", secondary=interests, backref="affiliates")

    def set_password(self, password):  # going to take a password and hash it
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
    url = db.Column(db.String(128), nullable=False)


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

  