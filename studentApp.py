from app import db
from app.Model.models import Campus, Interest
from flask_login import current_user
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request


# from app.Controller.forms import ClassForm, EditForm, EmptyForm
# from app.Model.models import Class, Major, Student
from flask_login import login_user, current_user, logout_user, login_required
from config import Config
from app import create_app


app = create_app(Config)


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    trigger = False
    if Campus.query.count() == 0:
        trigger = True
        campus = [
            "Washington State University(WSU)", "Ohio State University(OS)", "University of Washington(UW)"]

        for t in campus:
            db.session.add(Campus(name=t))

    if Interest.query.count() == 0:
        trigger = True
        interest = ["Carbon Cycling",
                    "Air quality",
                    "Evaporation",
                    "Flux measurement",
                    "Modeling",
                    "Drinking",
                    "Ground",
                    "Surface",
                    "Demand",
                    "Quality",
                    "Hydrology",
                    "Economics",
                    "Policy",
                    "Resource management",
                    "Lakes",
                    "Stream Ecology",
                    "Eutrophication",
                    "Ocean",
                    "Erosion",
                    "Deforestation",
                    "Wildfire",
                    "Land Use Change",
                    "Management",
                    "Climate",
                    "Agriculture",
                    "Geo Science",
                    "Human beings",
                    "Animals",
                    "Well being",
                    "Sociology",
                    "Anthropology",
                    "Governance",
                    "Migration",
                    "Demography",
                    "Philosophy",
                    "Communities",
                    "Political Science",
                    "Alternative fuel",
                    "Solar",
                    "Grid",
                    "Wind",
                    "Renewable",
                    "Supply",
                    "Soil Health",
                    "Other"
                    ]

        for t in interest:
            db.session.add(Interest(name=t))

    if trigger == True:
        db.session.commit()


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()


if __name__ == "__main__":
    app.run(debug=True)
