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
works_departments = db.Table(
    "works_departments",
    db.Column("affiliate_id", db.Integer, db.ForeignKey("affiliate.id")),
    db.Column("department_id", db.Integer, db.ForeignKey("department.id"))
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
    departments = db.relationship(
        "Department", secondary=works_departments, backref="affiliates"
    )
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

  #  parent_id = db.Column(db.Integer, db.ForeignKey('interest.id'))
   # parent = db.relationship('Interest', remote_side=[
    #                         id], backref='sub_interests')

# class Class(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     coursenum = db.Column(db.String(3))
#     title = db.Column(db.String(150))
#     major = db.Column(db.String(20),db.ForeignKey('major.name'))  #the major in the class model has to exist in the major class
#     roster=db.relationship('Enrolled',back_populates='classenrolled')
#     def __repr__(self):
#         return '<Class id: {} - coursenum: {}, title {}, major :{}>'.format(self.id,self.coursenum,self.title,self.major)
#     #this function gets the title
#     def getTitle(self): #all methods in a class has to have self in the parameters
#         return self.title


# class Major(db.Model):
#     name =  db.Column(db.String(20), primary_key=True)
#     department = db.Column(db.String(150))
#     classes = db.relationship('Class',backref='coursemajor',lazy='dynamic')#connects the major table to the class table
#     studentsinmajor = db.relationship('StudentMajor',back_populates='_major')
#     def __repr__(self):
#         return '<Majoir name: {} - department: {}>'.format(self.name,self.department)#  to print out in the command promt.
#     #manually delete the db file. im  not cool enough to do it automatically

# class Student(UserMixin,db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(64),unique=True,index=True)
#     password_hash = db.Column(db.String(128))
#     firstname = db.Column(db.String(128))
#     lastname = db.Column(db.String(128))
#     address = db.Column(db.String(200))
#     email = db.Column(db.String(128),unique=True,index=True)
#     last_seen=db.Column(db.DateTime,default=datetime.utcnow)
#     classes=db.relationship('Enrolled',back_populates='studentenrolled')
#     majorsofstudent = db.relationship('StudentMajor',back_populates='_student')
#     def __repr__(self):
#         return '<Student {} - {} {} -{};>'.format(self.id,self.firstname,self.lastname,self.email)


#     def set_password(self,password):#going to take a password and hash it
#         self.password_hash=generate_password_hash(password)

#     def check_password(self,password):
#         return check_password_hash(self.password_hash,password)

#     def enroll(self,newclass):
#         if not self.is_enrolled(newclass):
#             newEnrollment = Enrolled(classenrolled=newclass)
#             self.classes.append(newEnrollment)
#             db.session.commit()

#     def unenroll(self,oldclass):
#         if  self.is_enrolled(oldclass):
#             #we need to check if the student is enrolled
#             curEnrollment = Enrolled.query.filter_by(studentid=self.id).filter_by(classid=oldclass.id).first()
#             db.session.delete(curEnrollment)
#             db.session.commit()

#     def is_enrolled(self,newclass):
#         return (Enrolled.query.filter_by(studentid=self.id).filter_by(classid=newclass.id).count() > 0)


#     def enrolledCourses(self):
#         return self.classes

#     def getEnrolmentDate(self,theclass):
#         if self.is_enrolled(theclass):
#             return Enrolled.query.filter_by(studentid=self.id).filter_by(classid=theclass.id).first().enrolldate
#         else:
#             return None


# class Enrolled(db.Model):
#     studentid = db.Column(db.Integer,db.ForeignKey('student.id'),primary_key=True)#to make sure a student only be able to enrol once
#     classid = db.Column(db.Integer,db.ForeignKey('class.id'),primary_key=True)
#     enrolldate = db.Column(db.DateTime, default=datetime.utcnow)
#     studentenrolled = db.relationship('Student')
#     classenrolled = db.relationship('Class')
#     def __repr__(self):
#         return '<Enrollment class : {} student: {} date: {}>'.format(self.classenrolled,self.studentenrolled,self.enrolldate)


# class StudentMajor(db.Model):
#     studentmajor=db.Column(db.String(20),db.ForeignKey('major.name'),primary_key=True)
#     studentid = db.Column(db.Integer,db.ForeignKey('student.id'),primary_key=True)
#     startdate = db.Column(db.DateTime)
#     primary = db.Column(db.Boolean)
#     _student = db.relationship('Student')
#     _major = db.relationship('Major')
#     def __repr__(self):
#         return '<Studentmajor ({},{},{},{})>'.format(self.studentmajor,self.studentid,self.startdate,self.primary)
