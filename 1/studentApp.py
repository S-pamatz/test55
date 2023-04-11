from app import  db
from app.Model.models import Major
from flask_login import current_user
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request


from app.Controller.forms import ClassForm, EditForm, EmptyForm
from app.Model.models import Class, Major, Student
from flask_login import login_user,current_user,logout_user,login_required
from config import Config
from app import create_app


app = create_app(Config)
@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Major.query.count()==0:
        majors=[
            {'name':'CptS','department':'School of EECS'},
            {'name':'SE','department':'School of EECS'},
            {'name':'EE','department':'Mechanical Engineering'},
            {'name':'MATH','department':'Mathematics'},
        
        
        
        
        
        ]


        for t in majors:
            db.session.add(Major(name=t['name'],department=t['department']))
        db.session.commit()
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen= datetime.utcnow()

if __name__ == "__main__":
    app.run(debug=True)