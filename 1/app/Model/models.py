from datetime import datetime
from app import db, login
from enum import unique
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))
    #return Student.query.filter_by(id=id) 





#model is how it is stored in the db. ewach class has certain data that is stored
#forms is what the user sees. it is connected to html
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))
    title = db.Column(db.String(150))
    major = db.Column(db.String(20),db.ForeignKey('major.name'))  #the major in the class model has to exist in the major class 
    roster=db.relationship('Enrolled',back_populates='classenrolled')
    def __repr__(self):
        return '<Class id: {} - coursenum: {}, title {}, major :{}>'.format(self.id,self.coursenum,self.title,self.major)
    #this function gets the title
    def getTitle(self): #all methods in a class has to have self in the parameters
        return self.title


class Major(db.Model):
    name =  db.Column(db.String(20), primary_key=True)
    department = db.Column(db.String(150)) 
    classes = db.relationship('Class',backref='coursemajor',lazy='dynamic')#connects the major table to the class table
    studentsinmajor = db.relationship('StudentMajor',back_populates='_major')
    def __repr__(self):
        return '<Majoir name: {} - department: {}>'.format(self.name,self.department)#  to print out in the command promt. 
    #manually delete the db file. im  not cool enough to do it automatically
class Affiliate(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    wsuCampus=db.Column(db.String)
    department=db.Column(db.String)
    url=db.Column(db.String)
    email=db.Column(db.String)

    def set_password(self,password):#going to take a password and hash it
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Student(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    address = db.Column(db.String(200))
    email = db.Column(db.String(128),unique=True,index=True)
    last_seen=db.Column(db.DateTime,default=datetime.utcnow)
    classes=db.relationship('Enrolled',back_populates='studentenrolled')
    majorsofstudent = db.relationship('StudentMajor',back_populates='_student')
    def __repr__(self):
        return '<Student {} - {} {} -{};>'.format(self.id,self.firstname,self.lastname,self.email)


    def set_password(self,password):#going to take a password and hash it
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def enroll(self,newclass):
        if not self.is_enrolled(newclass):
            newEnrollment = Enrolled(classenrolled=newclass)
            self.classes.append(newEnrollment)
            db.session.commit()

    def unenroll(self,oldclass):
        if  self.is_enrolled(oldclass):
            #we need to check if the student is enrolled
            curEnrollment = Enrolled.query.filter_by(studentid=self.id).filter_by(classid=oldclass.id).first()
            db.session.delete(curEnrollment)
            db.session.commit()

    def is_enrolled(self,newclass):
        return (Enrolled.query.filter_by(studentid=self.id).filter_by(classid=newclass.id).count() > 0)
        

    def enrolledCourses(self):
        return self.classes

    def getEnrolmentDate(self,theclass):
        if self.is_enrolled(theclass):
            return Enrolled.query.filter_by(studentid=self.id).filter_by(classid=theclass.id).first().enrolldate
        else:
            return None



class Enrolled(db.Model):
    studentid = db.Column(db.Integer,db.ForeignKey('student.id'),primary_key=True)#to make sure a student only be able to enrol once
    classid = db.Column(db.Integer,db.ForeignKey('class.id'),primary_key=True)
    enrolldate = db.Column(db.DateTime, default=datetime.utcnow)
    studentenrolled = db.relationship('Student')
    classenrolled = db.relationship('Class')
    def __repr__(self):
        return '<Enrollment class : {} student: {} date: {}>'.format(self.classenrolled,self.studentenrolled,self.enrolldate)


class StudentMajor(db.Model):
    studentmajor=db.Column(db.String(20),db.ForeignKey('major.name'),primary_key=True)
    studentid = db.Column(db.Integer,db.ForeignKey('student.id'),primary_key=True)
    startdate = db.Column(db.DateTime)
    primary = db.Column(db.Boolean)
    _student = db.relationship('Student')
    _major = db.relationship('Major')
    def __repr__(self):
        return '<Studentmajor ({},{},{},{})>'.format(self.studentmajor,self.studentid,self.startdate,self.primary)
