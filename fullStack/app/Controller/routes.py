# Import Flask function for rendering templates
import json
import unicodedata
from urllib import response
from flask import Flask, render_template

from flask import render_template
from flask import Flask, jsonify
import base64
import csv
from flask import make_response, render_template, flash, redirect, url_for, request, Blueprint, jsonify
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from app import db
import pandas as pd
import secrets
import os
import app
from app.Controller.auth_forms import AddIntrest, AddIntrestOld, AddKeywords, affiliateRegister
from app.Controller.forms import AddEducationForm, AddExperiencesForm, Edit, EditForm, AddProjectsForm, EditInterest, EditInterestSmall, PublicationForm, ask, editPublication, editTagsForm
from app.Model.models import Affiliate, Air, BigInterest, Department, Education, Experience, Interest, IntrestTest, Project, Publication, Subcategory, Water, smallInterest, smallinterestform
from flask_login import login_user, current_user, logout_user, login_required
from config import Config
from flask import Flask
from flask_mail import Mail, Message
import requests
routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER


application = Flask(__name__)
# app1.config.from_object(Config)
# Flask-Mail Configuration
# Example: Outlook/Office 365 SMTP server
# https://stackoverflow.com/questions/17980351/flask-mail-not-sending-emails-no-error-is-being-reported
# https://stackoverflow.com/questions/28466384/python-flask-email-keyerror-keyerror-mail
application.config['MAIL_SERVER'] = 'smtp.office365.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_DEFAULT_SENDER'] = 'wsuaffiliateconfirmation@outlook.com'
application.config['MAIL_USERNAME'] = 'wsuaffiliateconfirmation@outlook.com'
application.config['MAIL_PASSWORD'] = 'changethislater!'
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USE_SSL'] = False

application.config['MAIL_DEBUG'] = True

application.config['MAIL_SUPPRESS_SEND'] = False
application.config['TESTING'] = False
application.config['DEBUG'] = False
mail = Mail(application)
#############


####################ARVIN
@routes_blueprint.route('/profileSearch', methods=['GET'])
@routes_blueprint.route('/landing/<initial>', methods=['GET'])
def profileSearch(initial=None):
    affiliates = Affiliate.query.all()

    if initial:
        # Filter affiliates by the first letter of the last name
        filtered_affiliates = [user for user in affiliates if user.lastname and user.lastname[0].upper() == initial]
    else:
        filtered_affiliates = affiliates

    # Ensure 'lastname' is not None and is not an empty string before accessing it
    last_name_initials = set(user.lastname[0].upper() for user in affiliates if user.lastname)

    return render_template('profileSearch.html', affiliates=affiliates, last_name_initials=sorted(last_name_initials))


@routes_blueprint.route('/landing', methods=['GET'])
def displayLanding():
    return render_template('displayLanding.html')

#################JAMES
@routes_blueprint.route('/add_projects/<user_id>', methods=["POST", "GET"])
@login_required
def add_projects(user_id):
    if int(user_id) == current_user.id or current_user.is_admin:
        afform = AddProjectsForm()
        afform.set_partners()
        if afform.validate_on_submit():
            user = Affiliate.query.filter_by(id=user_id).first()
            project = Project(name=afform.name.data, authorss=afform.authors.data,
                            year=afform.year.data, publisher=afform.publisher.data,
                            partners=afform.partners.data,
                            url=check_url(afform.url.data))
            user.projects.append(project)
            db.session.add(project)
            db.session.commit()
            flash("You have added {project_name}".format(
                project_name=project.name))
            
            if current_user.is_admin:
                return redirect(url_for("auth.admin_edit_profile", user_id=user_id))
            return redirect(url_for('routes.add_projects', user_id=user_id))

        return render_template('add_projects.html', title='Add Projects', form=afform, user_id=user_id)
    else:
        flash("You are not authorized.")
        return redirect(url_for("routes.index"))


@routes_blueprint.route('/add_experiences/<user_id>', methods=["POST", "GET"])
@login_required
def add_experiences(user_id):
    if int(user_id) == current_user.id or current_user.is_admin:
        afform = AddExperiencesForm()
        user = Affiliate.query.filter_by(id=user_id).first()
        if afform.validate_on_submit():
            if afform.date_to.data != "Present" and int(afform.date_to.data) < int(afform.date_from.data):
                flash("Invalid Date")
                return redirect(url_for('routes.add_experiences', user_id=user_id))
            experience = Experience(title=afform.title.data, location=afform.location.data,
                            date_from=afform.date_from.data, date_to=afform.date_to.data)
            user.experience.append(experience)
            db.session.add(experience)
            db.session.commit()
            flash("You have added {experience_name}".format(
                experience_name=experience.title))
            if current_user.is_admin:
                return redirect(url_for("auth.admin_edit_profile", user_id=user_id))
            return redirect(url_for('routes.add_experiences', user_id=user_id))

        return render_template('add_experience.html', title='Add Experiences', form=afform, user_id=user_id)
    else:
        flash("You are not authorized")
        return redirect(url_for("routes.index"))

@routes_blueprint.route('/add_education/<user_id>', methods=["POST", "GET"])
@login_required
def add_education(user_id):
    if int(user_id) == current_user.id or current_user.is_admin:
        afform = AddEducationForm()
        if afform.validate_on_submit():
            user = Affiliate.query.filter_by(id=user_id).first()
            education = Education(degree=afform.degree.data, title=afform.name.data,
                                year=afform.year.data, college=afform.college.data)
            user.education.append(education)
            db.session.add(education)
            db.session.commit()
            flash("You have added {education_name}".format(
                education_name=education.title))
            if current_user.is_admin:
                return redirect(url_for("auth.admin_edit_profile", user_id=user_id))
            return redirect(url_for('routes.add_education', user_id=user_id))
        
        return render_template('add_education.html', title='Add Education', form=afform, user_id=user_id)
    else:
        flash("You are not authorized")
        return redirect(url_for("routes.index"))


#DEBUG = True
#from flask.ext.mail import Mail, Message
# Flask-Mail Configuration

s = URLSafeTimedSerializer('Thisisasecret!')
#http://127.0.0.1:5000/scopus_search?full_name=Boll,%20Jan
@routes_blueprint.route('/scopus_search', methods=['GET'])
def scopus_search():
    base_url = "https://api.elsevier.com/content/search/scopus"
    api_key = "bb043bb9dd59b0773aa25ee46c55307a"  # Replace with your actual API key
   # api_key="7wIu7PY7cV8dXPxpaS744oKcXDsAhuAaDrM68GXi"
    professor_full_name = request.args.get('full_name')

    if professor_full_name:
        query = f"AUTHNAME(\"{professor_full_name}\")"
        search_url = f"{base_url}?query={query}"
        headers = {"X-ELS-APIKey": api_key}

        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return f"Error: {response.status_code}", response.status_code
    else:
        return "No professor's name provided", 400

#https://api.semanticscholar.org/api-docs/graph#tag/Author-Data/operation/get_graph_get_author_papers
#http://127.0.0.1:5000/semantic_scholar_author_search?author_name=Jan+Boll
@routes_blueprint.route('/semantic_scholar_author_search', methods=['GET'])# this gets the id
def semantic_scholar_author_search():
    base_url = "https://api.semanticscholar.org/graph/v1/author/search"
    s2_api_key = "7wIu7PY7cV8dXPxpaS744oKcXDsAhuAaDrM68GXi" 

    author_name = request.args.get('author_name')

    if author_name:
        query = author_name.replace(' ', '+')  # Format the query for the URL

        # Construct the URL with the query parameter
        search_url = f"{base_url}?query={query}"
        headers = {"x-api-key": s2_api_key}

        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        
        else:
            return f"Error: {response.status_code}", response.status_code
    else:
        return "No author name provided", 400
@routes_blueprint.route('/semantic_scholar_author_search_user_input', methods=['GET', 'POST'])
def semantic_scholar_author_search_user_input():
    if request.method == 'POST':
        base_url = "https://api.semanticscholar.org/graph/v1/author/search"
        s2_api_key = "7wIu7PY7cV8dXPxpaS744oKcXDsAhuAaDrM68GXi" 

        author_name = request.form.get('author_name')

        if author_name:
            query = author_name.replace(' ', '+')  # Format the query for the URL

            # Construct the URL with the query parameter
            search_url = f"{base_url}?query={query}"
            headers = {"x-api-key": s2_api_key}

            response = requests.get(search_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                print("hello ")
                print("This is my parse function")
                print(response)
                dictNameID = {}
                authors_data = data.get('data', [])
                if authors_data:  
                    for author in authors_data:
                        dictNameID[author['authorId']] = author['name']
               # print(dictNameID)
                paperDict={}#conecting names with the papers
                for key, items in dictNameID.items():
                    paperDict[items]=get_author_papers(key)
               
                #print(first_paper)
                   # print(items, " wrote ", type(get_author_papers(key)))
                parseDict={}
                for key, val in paperDict.items():
                  #  print("this is the val ",key, " this is the type ",type(val))
                    for key2,val2 in val.items():
                     #   print("the key is ",key2," the val is ",type(val2))
                       
                        parseDict[key]=val2
                list=[]
                for key, val in parseDict.items():
                 #   print("the key is ",key," the val is ",val)
                    #print(type(val))
                  # print(val[0])
                    list.append(val[0])
                   # print("\n\n")
                print(len(list))
                for val in list:
                    for val2 in val.items():
                        print("this is my val 2",val2)
                json_list = json.dumps(list)
                return redirect(url_for('routes.submit_publicationAPI', paper_info_list=json_list))
                  #  print("\n\n")
                #since there can be multiple papers, we only need to check the first one
             
               
            else:
                return f"Error: {response.status_Wcode}", response.status_code
        else:
            return "No author name provided", 400

    return render_template('author_search_form.html')

def parsepaper(dict):
   # for key, val in dict.items():
        #print("new key is ",key)
     #   for inner_key, inner_value in val.items():
          #  print(f"  {inner_key}: {inner_value}")
    tempDict={}
    tempDict[2248598385]="offset: 0 data: [{'paperId': '05773cdfc3ed666d4c677dfbcf643da5fa2bdf7d', 'title': 'Deciphering complex groundwater age distributions and recharge processes in a tropical and fractured volcanic aquifer system'}, {'paperId': '5fc96eeac89d8ec4c25de9d9a13277c131267dc0', 'title': 'Baseflow recession analysis in the inland Pacific Northwest of the United States'}]"
    tempDict[2086112355]="offset: 0 data: [{'paperId': '69de5db3f0c739b0f459fc54f47470d26cd56ec4', 'title': 'Isotope Discrimination of Source Waters, Flowpaths, and Travel Times at an Acid-Generating, Lead–Zinc–Silver Mine, Silver Valley, Idaho, USA'}]"
    for key, val in tempDict.items():
        data_value = val.split("data: ")[1]  # Extracting the data part
        data_entries = data_value.split("},")  # Splitting individual data entries
        for entry in data_entries:
            entry = entry.strip() + '}'  # Ensuring valid JSON format
            # Removing the "offset: 0 data: " part
            entry = entry.replace("offset: 0 data: ", "")
            print(entry)

   
def get_author_papers(author_id):
    s2_api_key = "7wIu7PY7cV8dXPxpaS744oKcXDsAhuAaDrM68GXi"  # Replace with your Semantic Scholar API key

    base_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    headers = {"x-api-key": s2_api_key}

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data  # Return the papers data
    else:
        return None  # Return None
#http://127.0.0.1:5000/semantic_scholar_author_papers?author_id=2248598385

@routes_blueprint.route('/semantic_scholar_author_papers', methods=['GET'])# this gets the id abd searches up papers
def semantic_scholar_author_papers():
    s2_api_key = "7wIu7PY7cV8dXPxpaS744oKcXDsAhuAaDrM68GXi"  # Replace with your Semantic Scholar API key
    author_id = request.args.get('author_id')

    if author_id:
        base_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
        headers = {"x-api-key": s2_api_key}

        response = requests.get(base_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return f"Error: {response.status_code}", response.status_code
    else:
        return "No author ID provided", 400




s2_api_key = "7wIu7PY7cV8dXPxpaS744oKcXDsAhuAaDrM68GXi"



#IRONMAN



import requests
#this is my rouyte that takes in the papers name and returns the list of authors
# i tested it with a small sample case and it seems to be returning the correct values
def semantic_scholar_paper_authors(paper_title):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    if paper_title:
        query = paper_title.replace(' ', '+') 

        # Construct the URL with the query parameter
        search_url = f"{base_url}?query={query}"
        headers = {"x-api-key": s2_api_key}

        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            papers_data = data.get('data', [])

            if papers_data:
                # Assuming we want information about the first paper in the result
                first_paper_id = papers_data[0]['paperId']

                # Make another request to get the authors of the paper
                paper_url = f"https://api.semanticscholar.org/graph/v1/paper/{first_paper_id}?fields=authors"
                paper_response = requests.get(paper_url, headers=headers)

                if paper_response.status_code == 200:
                    paper_data = paper_response.json()
                    author_data = paper_data.get('authors', [])

                    # Extract the list of names directly
                    author_names = [author.get('name') for author in author_data]

                    # Format names with a comma and a space
                    formatted_names = []
                    for name in author_names:
                        name_parts = name.split(',')
                        formatted_names.append(', '.join(name_parts).strip())

                    # Join the names with a comma and a space between every two names
                    author_names_formatted = ', '.join(formatted_names)

                    return [author_names_formatted]
                else:
                    return ["Error", f"Error {paper_response.status_code} when fetching paper authors"]
            else:
                return ["Error", "No papers found"]
        else:
            return ["Error", f"Error {response.status_code} when searching for papers"]
    else:
        return ["Error", "No paper title provided"]






#lock
@routes_blueprint.route('/submit_publicationAPI2', methods=['GET', 'POST'])
def submit_publicationAPI2():
    eform = PublicationForm()
    paper_info_list = request.args.get('paper_info_list')
    print("idk if this is what i am supposed to be doing")
    print(paper_info_list)
    if paper_info_list:
        # Convert the received JSON string back to a list of dictionaries
        paper_info_list = json.loads(paper_info_list)
       # print("GOKU ARE YOU THERE\n",paper_info_list)
    for n in range(3):
        #print(n, " is ",paper_info_list[n])
        pass
    titles = [item['title'] for item in paper_info_list]
    listTitle=[]
    for title in titles:
        print("GOKU ARE YOU THERE\n",title)
        listTitle.append(title)
    eform.title.data="is this being auto filled",
    if eform.validate_on_submit():
        # Create a new Publication object and associate it with the logged-in affiliate
        new_publication = Publication(
            authors=eform.authors.data,
            
            journal=eform.journal.data,
           # volume=eform.volume.data,
           # issue=eform.issue.data,
            publication_year=eform.publication_year.data,
          #  page_range=eform.page_range.data,
            affiliate=current_user  # Assuming "current_affiliate" is the logged-in user
        )
        db.session.add(new_publication)
        db.session.commit()
        flash('Publication submitted successfully!', 'success')
        return redirect(url_for('routes.index'))  # Redirect to the homepage after submission
    return render_template('submit_publication.html', form=eform)

#11_12
# i need to get the year that a paper too
def get_paper_publication_year(paper_id):
    # Get the paper ID from the request parameters
    
    
    if not paper_id:
        return jsonify({'error': 'Paper ID is required'}), 400

    # Make a GET request to the Semantic Scholar API
    api_url = f'https://api.semanticscholar.org/v1/paper/{paper_id}'
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        paper_data = response.json()
        
        # Extract the publication year
        publication_year = str(paper_data.get('year', 'Publication year not available'))
        return publication_year
      #  return jsonify({'paper_id': paper_id, 'publication_year': publication_year})
    else:
        return jsonify({'error': f'Unable to retrieve paper information. Status code: {response.status_code}'}), 500
    
# i need to get the volume of the paper lets code that up real quiock using the above route as our base
def get_paper_details_volume(paper_id):
    # Get the paper details from the Semantic Scholar API
    
    if not paper_id:
        return jsonify({'error': 'Paper ID is required'}), 400

    # Make a GET request to the Semantic Scholar API
    api_url = f'https://api.semanticscholar.org/v1/paper/{paper_id}'
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        paper_data = response.json()

        
   
        paper_volume = str(paper_data.get('volume', 'volume not available'))
        return paper_volume
    else:
        return jsonify({'error': f'Unable to retrieve paper information. Status code: {response.status_code}'}), 500
def get_paper_DOI(paper_id):
    # Get the paper details from the Semantic Scholar API
    
    if not paper_id:
        return jsonify({'error': 'Paper ID is required'}), 400

    # Make a GET request to the Semantic Scholar API
    api_url = f'https://api.semanticscholar.org/v1/paper/{paper_id}'
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        paper_data = response.json()

       
        doi = str(paper_data.get('doi', 'DOI not available'))

        return {
          
            'doi': doi,
        }
    else:
        return jsonify({'error': f'Unable to retrieve paper information. Status code: {response.status_code}'}), 500
#one of your girls
def get_author_names_title(title):
   

   #return current_publication.title
    authors = semantic_scholar_paper_authors(title)

    cleaned_authors = ' '.join([remove_unicode_escape_sequences(author) for author in authors])
    print(type(cleaned_authors))
    return cleaned_authors
@routes_blueprint.route('/submit_publicationAPI', methods=['GET', 'POST'])
def submit_publicationAPI():
    eform = PublicationForm()
    paper_info_list = request.args.get('paper_info_list')

    if paper_info_list:
        
        paper_info_list = json.loads(paper_info_list)

    # Extract titles from the paper_info_list
    titles = [item['title'] for item in paper_info_list]
    print("GOKU ARE YOU THERE\n", titles)
    paperID = [item['paperId'] for item in paper_info_list]
    print("this is my paperid", paperID)
    # Get the name of the affiliate from current_user object
    publishDATE = [get_paper_publication_year(paper_id) for paper_id in paperID]
    print(publishDATE)
    paperDOI=[get_paper_DOI(paper_id) for paper_id in paperID]
    print("here are my paper DOI",paperDOI)
    print("why is are  breaking. are u stupid like me? ",len(paperDOI))
    name=current_user.firstname+" "+current_user.lastname
    print("this is the name",name)
    print("this is the type of my titles", type(titles))
    print("why are u breaking plz stop ",titles)
    print("this is the type of my publishdate",type(publishDATE))
    print(len(publishDATE))
   
    for x in range(len(publishDATE)):
        authors=get_author_names_title(titles[x])
        new_publication = Publication(
            title=titles[x], 
            authors=authors,
            affiliate=current_user,
            publication_year=publishDATE[x],
            journal=paperDOI[x].get('doi', 'DOI not available')
            
            
        )
        db.session.add(new_publication)
        db.session.commit() 
   

    

    return redirect(url_for('routes.index'))

#manually inputting
@routes_blueprint.route('/submit_publication', methods=['GET', 'POST'])
def submit_publication():
    form = PublicationForm()
    if form.validate_on_submit():
        # Create a new Publication object and associate it with the logged-in affiliate
        new_publication = Publication(
            authors=form.authors.data,
            title=form.title.data,
            journal=form.journal.data,
            volume=form.volume.data,
            issue=form.issue.data,
            publication_year=form.publication_year.data,
            page_range=form.page_range.data,
            affiliate=current_user  # Assuming "current_affiliate" is the logged-in user
        )
        db.session.add(new_publication)
        db.session.commit()
        flash('Publication submitted successfully!', 'success')
        return redirect(url_for('routes.index'))  # Redirect to the homepage after submission
    return render_template('submit_publication.html', form=form)


@routes_blueprint.route('/mypub')
def mypub():
    if current_user:
        publications = Publication.query.filter_by(affiliate=current_user).all()
        return render_template('myPub.html', publications=publications)
    else:
        # Handle case if no user is logged in
        return render_template('error.html', message="No user logged in")  # Or redirect to login, etc.
    
@routes_blueprint.route('/delete_publication/<int:publication_id>', methods=['GET', 'POST'])
def delete_publication(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    
    # Check if the current user has the authorization to delete this publication
    if publication.affiliate == current_user:
        db.session.delete(publication)
        db.session.commit()
        flash('Publication deleted successfully!', 'success')
    else:
        flash('You are not authorized to delete this publication', 'danger')

    return redirect(url_for('routes.index'))







################################################
#code above is for api
###########################################
@routes_blueprint.route('/email/<givenEmail>', methods=['GET', 'POST'])
def email(givenEmail):
    if request.method == 'GET':

        # email = request.form['email']
        print("1")
        email = givenEmail
        print(email)
        token = s.dumps(email, salt='email-confirm')
        print("2")
        msg = Message(
            'Confirm Email', sender='wsuaffiliateconfirmation@outlook.com', recipients=[email])
        print("3")
        link = url_for('routes.confirm_email', token=token,
                       _external=True)  # look at later
        print("this is test\n")
        print(application.config['MAIL_SERVER'])
        print(application.config['MAIL_PORT'])
        msg.body = 'Your link is {}'.format(link)
    # msg.body="test"ws1
    # g@gmail.com

        try:
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", str(e))

       # return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
        return 'email sending...please check email'


@routes_blueprint.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)

    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

    return redirect(url_for('routes.tData', givenEmail=email))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(Config.STATIC_FOLDER, picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@routes_blueprint.route('/home', methods=['GET'])
def tempIndex():
    return render_template('cereoLink.html')

def test_saved_tags1():
    user_interests = current_user.interests
    combined_data = {}

    for interest in user_interests:
        interest_name = interest.name
        subcategory_name = interest.subcategory.name if interest.subcategory else None

        if interest_name not in combined_data:
            combined_data[interest_name] = {
                "Interest": interest_name, "SubCategories": []}

        if subcategory_name:
            combined_data[interest_name]["SubCategories"].append(
                subcategory_name)

    result_data = list(combined_data.values())

    # Return the combined data directly
    return result_data
@routes_blueprint.route('/index', methods=['GET'])
@routes_blueprint.route('/', methods=['GET'])
@login_required
def index():
    publications = Publication.query.filter_by(affiliate=current_user).all()
       
    #eform = EmptyForm()
    image_file = url_for('static', filename=current_user.image_file)
    # Assuming 'interests' is the relationship between Affiliate and IntrestTest
    categories = current_user.interests
    combined_data=test_saved_tags1()
    print("this is a test",combined_data)
    # Retrieve all subcategories related to the current user's categories
    subcategories = []
    for category in categories:
        subcategories.extend(category.subcategory.interests)
    subcategory_names = [subcategory.name for subcategory in subcategories]
    print(subcategory_names)

    print(categories)
    return render_template('display_profile.html', title='Display Profile', affiliate=current_user, image_file=image_file, combined_data= combined_data,publications=publications)








def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(Config.STATIC_FOLDER, picture_fn)
    form_picture.save(picture_path)

    return picture_fn


#

@routes_blueprint.route('/get_subcategories/<selected_interest_id>', methods=['GET'])
def get_subcategories(selected_interest_id):
    selected_interest = IntrestTest.query.get(selected_interest_id)

    if selected_interest:
        subcategories = selected_interest.subcategory
        subcategory_options = ''

        # Ensure subcategories are retrieved as a list
        if not isinstance(subcategories, list):
            subcategories = [subcategories]

        for subcategory in subcategories:
            subcategory_options += f'<option value="{subcategory.id}">{subcategory.name}</option>'

        if subcategory_options:
            return subcategory_options

    return 'No subcategories found for the given interest.'

    # Return an empty string if no matching interest is found
    return ''

    # Return an empty string if no matching interest is found
    return ''

@routes_blueprint.route('/test_saved_tags', methods=['GET'])
def test_saved_tags():
    user_interests = current_user.interests
    combined_data = {}

    for interest in user_interests:
        interest_name = interest.name
        subcategory_name = interest.subcategory.name if interest.subcategory else None

        if interest_name not in combined_data:
            combined_data[interest_name] = {
                "Interest": interest_name, "SubCategories": []}

        if subcategory_name:
            combined_data[interest_name]["SubCategories"].append(
                subcategory_name)

    result_data = list(combined_data.values())

    return jsonify({
        current_user.email: result_data
    })

@routes_blueprint.route('/addTags', methods=['GET', 'POST'])
@login_required
def addTags():
    # Fetch interests and subcategories
   # Fetch distinct interests
    interests = db.session.query(IntrestTest).distinct(IntrestTest.name).order_by(IntrestTest.name).all()
    subcategories = Subcategory.query.all()

    # Instantiate the form
    eform = editTagsForm()

    # Populate form choices
    eform.areaofinterest.choices = [
        (interest.id, interest.name) for interest in interests]
    eform.subcategory.choices = [(subcategory.id, subcategory.name)
                                 for subcategory in subcategories]
    if request.method == 'POST' and eform.validate_on_submit():
        selected_interest_id = eform.areaofinterest.data
        selected_interest = IntrestTest.query.get(selected_interest_id)

        # Update the user's interests#
        current_user.interests.append(selected_interest)

        # Now, you can access the subcategory through the selected_interest
        selected_subcategory = selected_interest.subcategory

        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('routes.addTags'))

    # If it's a GET request or the form didn't validate, render the template
    return render_template('addTags.html', title='Add Tags', form=eform, interests=interests, subcategories=subcategories)

@routes_blueprint.route('/edit_education/<user_id>/<education_id>', methods=['POST', 'GET'])
@login_required
def edit_education(education_id, user_id):
    if int(user_id) == current_user.id or current_user.is_admin:
        afform = AddEducationForm()
        current_education = Education.query.filter_by(id=education_id).first()
        if afform.validate_on_submit():
            current_education.degree = afform.degree.data
            current_education.title = afform.name.data
            current_education.college = afform.college.data
            current_education.year = afform.year.data
            db.session.add(current_education)
            db.session.commit()
            flash("You have modified {education_name}".format(
                education_name=current_education.title))
            if current_user.is_admin:
                return redirect(url_for('auth.admin_edit_profile', user_id=user_id))
            return redirect(url_for('routes.index'))
        
        elif request.method == 'GET':
            afform.degree.data = current_education.degree
            afform.name.data = current_education.title
            afform.college.data = current_education.college

        return render_template('edit_education.html', title='Edit Education', form=afform, education_id=education_id, user_id=user_id)
    else:
        flash("You are not authorized")
        return redirect(url_for("routes.index"))
    
@routes_blueprint.route('/edit_exp/<user_id>/<exp_id>', methods=['POST', 'GET'])
@login_required
def edit_experience(exp_id, user_id):
    if int(user_id) == current_user.id or current_user.is_admin:
        afform = AddExperiencesForm()
        current_exp = Experience.query.filter_by(id=exp_id).first()
        if afform.validate_on_submit():
            current_exp.title = afform.title.data
            current_exp.location = afform.location.data
            current_exp.date_from = afform.date_from.data
            current_exp.date_to = afform.date_to.data
            db.session.add(current_exp)
            db.session.commit()
            flash("You have modified {current_exp_name}".format(
                current_exp_name=current_exp.title))
            if current_user.is_admin:
                return redirect(url_for('auth.admin_edit_profile', user_id=user_id))
            return redirect(url_for('routes.index'))
        
        elif request.method == 'GET':
            afform.title.data = current_exp.title
            afform.location.data = current_exp.location
            afform.date_from.data = current_exp.date_from
            afform.date_to.data = current_exp.date_to

        return render_template('edit_experience.html', title='Edit Professional Experience', form=afform, exp_id=exp_id, user_id=user_id)
    else:
        flash("You are not authorized")
        return redirect(url_for("routes.index"))
@routes_blueprint.route('/edit_publication/<publication_id>', methods=['POST', 'GET'])
@login_required
def edit_publication(publication_id):
    afform = PublicationForm()
    current_publication = Publication.query.filter_by(id=publication_id).first()
    if afform.validate_on_submit():
        current_publication.authors = afform.authors.data
        current_publication.title = afform.title.data
        current_publication.publication_year = afform.publication_year.data
        current_publication.journal = afform.journal.data
      #  current_publication.volume = afform.volume.data
     #   current_publication.issue = afform.issue.data
      #  current_publication.page_range = afform.page_range.data
        db.session.add(current_publication)
        db.session.commit()
        flash("You have modified {current_publication_name}".format(
            current_publication_name=current_publication.title))
        return redirect(url_for('routes.index'))
    
    elif request.method == 'GET':
        afform.title.data = current_publication.title
        afform.authors.data = current_publication.authors
        afform.publication_year.data = current_publication.publication_year
        afform.journal.data = current_publication.journal
     #   afform.volume.data = current_publication.volume
    #    afform.issue.data = current_publication.issue
    #    afform.page_range.data = current_publication.page_range

    return render_template('edit_Publication.html', title='Edit Publication', form=afform, publication_id=publication_id)



def remove_unicode_escape_sequences(author_name):
    return unicodedata.normalize("NFKD", author_name)
#one of 
def edit_publication_add_parse(publication_id):
   
    current_publication = Publication.query.filter_by(id=publication_id).first()
   #return current_publication.title
    authors = semantic_scholar_paper_authors(current_publication.title)
    test= semantic_scholar_paper_authors( current_publication.title)
    cleaned_authors = ' '.join([remove_unicode_escape_sequences(author) for author in authors])
    print(type(cleaned_authors))
    return cleaned_authors

#one of your girls tonight~
@routes_blueprint.route('/edit_publication_add/<publication_id>', methods=['POST', 'GET'])
@login_required
def edit_publication_add(publication_id):
    afform = PublicationForm()
    authors=edit_publication_add_parse(publication_id)# returns list of authors
    current_publication = Publication.query.filter_by(id=publication_id).first()#print paper id
    

    # Update current_publication.authors with the form data
    current_publication.authors = authors
    print(authors)
    # Save the changes
    db.session.commit()


    return redirect(url_for('routes.index'))


@routes_blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    image_file = url_for('static', filename=current_user.image_file)
    eform = EditForm()
    eform.set_department_choices()
    eform.set_university_choices()
  #  eform.set_partners()

    department_name = eform.department.data
    print("Department Name from Form:", department_name)

    department = Department.query.filter_by(name=department_name).first()
    publications = Publication.query.filter_by(affiliate=current_user).all()

    if request.method == 'POST' and eform.validate_on_submit():
        if eform.picture.data:
            picture_file = save_picture(eform.picture.data)
            current_user.image_file = picture_file

        current_user.firstname = eform.firstname.data
        current_user.lastname = eform.lastname.data
        current_user.wsuCampus = eform.campus.data
        current_user.university = eform.university.data
      #  current_user.partners = eform.partners.data
        current_user.URL = eform.URL.data

        if eform.password.data:
            current_user.set_password(eform.password.data)

        department_name = eform.department.data
        print("1", department_name)
        department = Department.query.filter_by(name=department_name).first()
        print("2", department)
        if department:
            print("1")
            current_user.departments = [department]
            print("3", current_user.departments)
            current_user.department = department_name
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('routes.index'))

    elif request.method == 'GET':
        eform.firstname.data = current_user.firstname
        eform.lastname.data = current_user.lastname
        eform.campus.data = current_user.wsuCampus
        eform.university.data = current_user.university
      #  eform.partners.data = current_user.partners

        if current_user.departments:
            eform.department.data = current_user.departments[0].name

      
     
    eform.URL.data = current_user.URL if hasattr(current_user, 'URL') else None


    return render_template('edit_profile.html', title='Edit Profile', form=eform, image_file=image_file, affiliate=current_user, publications=publications)


@routes_blueprint.route('/edit_project/<user_id>/<project_id>', methods=['POST', 'GET'])
@login_required
def edit_project(project_id, user_id):
    if int(user_id) == current_user.id or current_user.is_admin:
        afform = AddProjectsForm()
        afform.set_partners()
        current_project = Project.query.filter_by(id=project_id).first()
        if afform.validate_on_submit():
            current_project.name = afform.name.data
            current_project.authorss = afform.authors.data
            current_project.year = afform.year.data
            current_project.publisher = afform.publisher.data
            current_project.partners = afform.partners.data
            current_project.url = afform.url.data
            db.session.add(current_project)
            db.session.commit()
            flash("You have modified {current_project_name}".format(
                current_project_name=current_project.name))
            if current_user.is_admin:
                return redirect(url_for("auth.admin_edit_profile", user_id=user_id))
            return redirect(url_for('routes.edit_profile'))
        
        elif request.method == 'GET':
            afform.name.data = current_project.name
            afform.authors.data = current_project.authorss
            afform.publisher.data = current_project.publisher
            afform.url.data = current_project.url
            afform.partners.data=current_project.partners
            afform.year.data=current_project.year
        return render_template('edit_project.html', title='Edit Project', form=afform, project_id=project_id, user_id=user_id)
    else:
        flash("You are not authorized")
        return redirect(url_for("routes.index"))

@routes_blueprint.route('/displayAllUsers', methods=['GET', 'POST'])
def displayAll():
    # print("test")

    # users = Affiliate.query.all()
    # image_urls = []

    # # Loop through the users and generate image URLs
    # for user in users:
    #     image_file = url_for('static', filename=user.image_file)
    #     image_urls.append(image_file)

    # # Combine users and image_urls into a list of tuples
    # user_data = zip(users, image_urls)

    return render_template('displayAll.html', user_data=[])


def check_url(url):
    if "https://" in url or "http://" in url:
        if "https://" in url:
            new_url = url[7:]
            return new_url
        else:
            new_url = url[6:]
            return new_url
    else:
        return url


@routes_blueprint.route('/readFile', methods=['GET', 'POST'])
def read():
    df = pd.read_csv("db.csv", usecols=['Email'])
    if request.method == 'GET':
        return '<form action="/readFile" method="POST"><input name="email"><input type="submit"></form>'
    email = request.form['email']

    return redirect(url_for('routes.email', givenEmail=email))
   # email = request.form['email']
   # if (readFile(email) == True):
    #flash("this email is in our db. we will re-route you to the validation page")
    #  return redirect(url_for('routes.email', givenEmail=email))
    # return redirect(url_for('routes.tData', givenEmail=email))
 #   else:
    # flash("this email is not in our db. we will redirect you to the register page")
    #  return redirect(url_for('auth.register'))


def readFile(email):
    df = pd.read_csv("db.csv", usecols=['Email', 'Name', 'Department'])
    print(type(df))
    if email in df['Email'].values:
        return True
    else:
        return False


def getMail(email):
    listInfo = []
    df = pd.read_csv("db.csv", usecols=[
                     'Email', 'Name', 'Department', 'URL', 'WSU Campus'])

    if email in df['Email'].values:
        # Access 'Name' and 'Department' values based on the condition
        name = df[df['Email'] == email]['Name'].values[0]
        department = df[df['Email'] == email]['Department'].values[0]
        url = df[df['Email'] == email]['URL'].values[0]

        campus = df[df['Email'] == email]['WSU Campus'].values[0]
        print(f"Name: {name}")
        fullName = name.split(" ")
        print(f"Department: {department}")
        print(f"url: {url}")
  #  print(f"URL: {url}")
        listInfo.append(email)  # index 0
        listInfo.append(fullName[0])  # first#index 1
        listInfo.append(fullName[1])  # last#index 2

        listInfo.append(campus)  # index 3
        listInfo.append(url)  # index 4
        listInfo.append(department)

    return listInfo


@routes_blueprint.route('/tData/<givenEmail>', methods=['GET', 'POST'])
def tData(givenEmail):
    rform = affiliateRegister()
    list1 = getMail(givenEmail)

    rform.email.default = list1[0]
    rform.firstname.default = list1[1]
    rform.lastname.default = list1[2]
    rform.wsuCampus.default = list1[3]
    rform.url.default = list1[4]
    rform.department.default = list1[5]
    rform.process()
    print(list1)
    print("this is the given email ", givenEmail)
    if rform.validate_on_submit():
        affiliate = Affiliate(firstname=rform.firstname.data,
                              lastname=rform.lastname.data,
                              wsuCampus=rform.wsuCampus.data,

                              url=rform.url.data,
                              validUser="Valid",
                              email=list1[0])
        affiliate.set_password(rform.password.data)

        db.session.add(affiliate)
        db.session.commit()
        flash('You are  a registered user')
  #  return redirect(url_for('routes.index'))

    return render_template('register.html', form=rform, emailTest=list1[0])


@routes_blueprint.route('/jsnDerulo', methods=['GET'])
def jsonD():
    jsonData = []

    affiliates = Affiliate.query.all()
    for user in affiliates:
        # Create a dictionary to store interests grouped by subcategory
        interests_data = {}

        for interest in user.interests:
            subcategory_name = interest.subcategory.name if interest.subcategory else "Other"
            if interest.name not in interests_data:
                interests_data[interest.name] = []
            interests_data[interest.name].append(subcategory_name)

        # Convert the subcategory lists to sets and then back to lists to remove duplicates
        for interest_name in interests_data:
            interests_data[interest_name] = list(
                set(interests_data[interest_name]))
        print(interests_data)
        jsonData.append({
            "firstName": user.firstname,
            "lastName": user.lastname,
            "wsu campus": user.wsuCampus,
            "membership": user.membership,
            "email": user.email,
            "interests": interests_data
        })

    # Convert the data to a JSON string
    json_data = jsonify(jsonData)
    print(json_data)
    # Create a Response with the JSON data and set headers for download
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=affiliates.json"
    response.headers["Content-Type"] = "application/json"

    return response


@routes_blueprint.route('/jsnKey', methods=['GET'])
def jsonK():
    print("sd")
    jsonDey = []

    intrests = Interest.query.all()

    for i in intrests:
       # print(user.email)
        jsonDey.append({
            "intrest": i.name,

        })
    # Convert the data to a JSON string
    json_data = jsonify(jsonDey)

    # Create a Response with the JSON data and set headers for download
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=affiliates.json"
    response.headers["Content-Type"] = "application/json"

    return response

    # You can now use the 'keywords' list to process all the entered keywords.


@routes_blueprint.route('/tagTest', methods=['GET'])
def tagTest():
    jsonData = []

    tags = Interest.query.all()
    for tag in tags:
        tag_data = {
            'id': tag.id,
            'name': tag.name
        }
        jsonData.append(tag_data)

    return jsonify(jsonData)


# this is just to create big instances

# initial;

# this will be used to connect
@routes_blueprint.route('/createIntrests', methods=['GET', 'POST'])
def createIntrests():
    eForm = AddIntrest()
    eForm.subcategory_id.choices = [
        (subcategory.id, subcategory.name) for subcategory in Subcategory.query.all()]

    if eForm.validate_on_submit():
        # Check if the interest already exists in the database
        existing_interest = IntrestTest.query.filter_by(
            name=eForm.name.data).first()
        print("hi")
       # if existing_interest:
        #    flash("Interest already exists", "warning")
        #   return redirect(url_for('routes.createIntrests'))

        # If the interest doesn't exist, add it to the database
        interest = IntrestTest(
            name=eForm.name.data,
            subcategory_id=eForm.subcategory_id.data
        )
        db.session.add(interest)
        db.session.commit()

        # Add a success message
        flash("Interest added successfully", "success")
        # Redirect back to the form page
        return redirect(url_for('routes.createIntrests'))
    else:

        # Print out form errors to see why validation failed
        print(eForm.errors)
    return render_template('createIntrests.html', form=eForm)


@routes_blueprint.route('/createIntrestsRepeat', methods=['GET', 'POST'])
def createIntrestsRepeat():
    eForm = AddIntrestOld()

    # Fetch unique interest names from your database
    unique_interest_names = list(
        set(interest.name for interest in IntrestTest.query.all()))

    # Fetch unique subcategory names from your database
    unique_subcategory_names = list(
        set(subcategory.name for subcategory in Subcategory.query.all()))

    # Populate the dropdowns with unique interest and subcategory names
    eForm.name.choices = [(name, name) for name in unique_interest_names]
    eForm.subcategory_id.choices = [(name, name)
                                    for name in unique_subcategory_names]

    if eForm.validate_on_submit():
        # Get the selected values from the form
        selected_interest_name = eForm.name.data
        selected_subcategory_name = eForm.subcategory_id.data

        # Find the corresponding interest and subcategory records based on their names
        interest = IntrestTest.query.filter_by(
            name=selected_interest_name).first()
        subcategory = Subcategory.query.filter_by(
            name=selected_subcategory_name).first()

        # Create a new IntrestTest record with the selected interest and subcategory
        new_interest = IntrestTest(
            name=interest.name,
            subcategory=subcategory
        )

        db.session.add(new_interest)
        db.session.commit()

        # Add a success message
        flash("Interest added successfully", "success")
        # Redirect back to the form page
        return redirect(url_for('routes.createIntrestsRepeat'))

    return render_template('createIntrestsRepeat.html', form=eForm)


@routes_blueprint.route('/displayAllIntrests', methods=['GET', 'POST'])
def displayIntrests():
    interests = IntrestTest.query.order_by(IntrestTest.name).all()
    return render_template('displayIntrestsAll.html', title="Tags", interests=interests)


@routes_blueprint.route('/displaySubCategory', methods=['GET', 'POST'])
def displayDub():
    interests = IntrestTest.query.order_by(IntrestTest.name).all()
    return render_template('displaySub.html', title="Interests", interests=interests)


@routes_blueprint.route('/interests_json', methods=['GET'])
def interests_json():
    data = []

    interests = IntrestTest.query.order_by(IntrestTest.name).all()

    for interest in interests:
        interest_data = {
            "Interest": interest.name,
            "Subcategory": None
        }

        if interest.subcategory:
            interest_data["Subcategory"] = interest.subcategory.name

        data.append(interest_data)

    # Convert the data to a JSON response
    json_data = jsonify(data)

    # Create a Response with the JSON data and set headers for download
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=affiliates.json"
    response.headers["Content-Type"] = "application/json"

    return response


@routes_blueprint.route('/testSub', methods=['GET'])
def testSub():

    data = []

    # Assuming you have a makeDictFromIntrests function
    interest_dict = makeDictFromIntrests()

    # Convert the dictionary to a list of dictionaries
    for interest, subcategories in interest_dict.items():
        data.append({
            "Interest": interest,
            "Subcategories": subcategories
        })

    # Convert the data to a JSON response
    json_data = jsonify(data)

    # Create a Response with the JSON data
    response = make_response(json_data)
    response.headers["Content-Disposition"] = "attachment; filename=intrests.json"
    response.headers["Content-Type"] = "application/json"
    return response


def makeDictFromIntrests():

    dict1 = {}
    t = 1
    interests = IntrestTest.query.order_by(IntrestTest.name).all()
    for interest in interests:
        if interest.name in dict1:
            dict1[interest.name].append(interest.subcategory.name)
        else:
            dict1[interest.name] = [
                interest.subcategory.name] if interest.subcategory else []

    return dict1


# TAY
@routes_blueprint.route('/get_all_interests1', methods=['GET'])
def get_all_interests():
    # Perform a query to retrieve all IntrestTest objects with their associated subinterests
    all_interests = IntrestTest.query.all()

    # Create a dictionary to store the results
    results = {}

    for interest_test in all_interests:
        subcategory = interest_test.subcategory
        if subcategory:
            intrest_test_name = interest_test.name
            subinterest_name = subcategory.name
            if intrest_test_name not in results:
                results[intrest_test_name] = []
            results[intrest_test_name].append(subinterest_name)

    # Create a JSON response
    response = {
        "interests": results
    }

    # Return the JSON response
    return jsonify(response)


@routes_blueprint.route('/search_interests', methods=['GET'])
def search_interests():
    # Get the search query from the request
    # Assuming the query parameter is named 'query'
    search_query = request.args.get('query')

    # Perform a query to retrieve interests matching the search query
    matching_interests = IntrestTest.query.filter(
        IntrestTest.name.ilike(f"%{search_query}%")).all()

    # Create a set to store unique subinterests
    unique_subinterests = set()

    for interest_test in matching_interests:
        subcategory = interest_test.subcategory
        if subcategory:
            subinterest_name = subcategory.name
            unique_subinterests.add(subinterest_name)

    # Create a JSON response
    response = {
        "data":
        list(unique_subinterests)

    }

    # Return the JSON response
    return jsonify(response)
#TEAMv
#http://127.0.0.1:5000/search?inputValue=James%20Lim
@routes_blueprint.route('/search', methods=['GET'])
def search():
    inputValue = request.args.get("inputValue")

    # Search through the relevant fields for the inputValue
    affiliates = db.session.query(Affiliate).filter(
        Affiliate.firstname.ilike(f"%{inputValue}%") |
        Affiliate.lastname.ilike(f"%{inputValue}%") |
        Affiliate.wsuCampus.ilike(f"%{inputValue}%") |
        Affiliate.department.ilike(f"%{inputValue}%") |
        Affiliate.email.ilike(f"%{inputValue}%") |
        Affiliate.url.ilike(f"%{inputValue}%")
    ).all()

    # Construct the response data
    response_data = []
    for affiliate in affiliates:
        response_data.append({
            "Interest": '',
            "Department": getattr(affiliate, 'department', ''),
            "Name": f"{getattr(affiliate, 'firstname', '')} {getattr(affiliate, 'lastname', '')}".strip(),
            "Membership": '',  # placeholder, adjust as needed
            "WSUCampus": getattr(affiliate, 'wsuCampus', ''),
            "Email": getattr(affiliate, 'email', ''),
            "URL": getattr(affiliate, 'url', '')
        })
    return jsonify(response_data)


################I WISH I CAN NOT CODE FOR 2 DAYS IN A ROW
#http://localhost:5000/searchSAD?inputValue=small1
@routes_blueprint.route('/searchSAD', methods=['GET'])
def searchSAD():
    inputValue = request.args.get("inputValue")

    # Search through the relevant fields for the inputValue
    affiliates = db.session.query(Affiliate).join(smallInterest).filter(
        smallInterest.name.ilike(f"%{inputValue}%") |
        Affiliate.firstname.ilike(f"%{inputValue}%") |
        Affiliate.lastname.ilike(f"%{inputValue}%") |
        Affiliate.wsuCampus.ilike(f"%{inputValue}%") |
        Affiliate.department.ilike(f"%{inputValue}%") |
        Affiliate.email.ilike(f"%{inputValue}%") |
        Affiliate.url.ilike(f"%{inputValue}%") |
        BigInterest.name.ilike(f"%{inputValue}%")
    ).all()

    # Construct the response data
    response_data = []
    for affiliate in affiliates:
        big_interests = [interest.name for interest in affiliate.bigInterest]
        small_interests = [interest.name for interest in affiliate.smallInterest if interest.name.lower() == inputValue.lower()]

        response_data.append({
            "Interest": {
                "Big": big_interests,
                "Small": small_interests
            },
            "Department": getattr(affiliate, 'department', ''),
            "Name": f"{getattr(affiliate, 'firstname', '')} {getattr(affiliate, 'lastname', '')}".strip(),
            "Membership": '',  # placeholder, adjust as needed
            "WSUCampus": getattr(affiliate, 'wsuCampus', ''),
            "Email": getattr(affiliate, 'email', ''),
            "URL": getattr(affiliate, 'url', '')
        })
    return jsonify(response_data)



@routes_blueprint.route('/search_Unique_interests', methods=['GET'])
def search_unique_interests():
    # Get the search query from the request
    # Assuming the query parameter is named 'query'
    #search_query = request.args.get('query')

    # Perform a query to retrieve interests matching the search query
    allI = IntrestTest.query.all()
    uI = set()  # makes it
    for interest_test in allI:
        interest_name = interest_test.name
        uI.add(interest_name)
    # Create a JSON response
    response = {
        "data":
        list(uI)

    }

    # Return the JSON response
    return jsonify(response)


@routes_blueprint.route('/returnUniqueDepart', methods=['GET'])
def returnUniqueDepart():
    all_departments = Department.query.all()

    unique_names = set()  # Use set to ensure unique department names

    for dept in all_departments:
        unique_names.add(dept.name)

    # Convert the set of unique names to a sorted list
    sorted_names = sorted(list(unique_names))

    return jsonify(sorted_names)

    # Get the search query from the request
    # Assuming the query parameter is named 'query'
    #search_query = request.args.get('query')

    # Perform a query to retrieve interests matching the search query
    # checkList = [
    #     ("Biology", "Bio"),
    #     ("Computer Science", "CS"),
    #     ("College of Nursing", "CoN"),
    #     ("Civil and Environmental Engineering", "CEE"),
    #     ("Edward R. Murrow", "ERMC"),
    #     ("Anthropology", "Anthro"),
    #     ("Hydraulic and Water Resource Engineering", "HWRE"),
    #     ("School of the Environment", "SoE"),
    #     ("First-Year Programs", "FYP"),
    #     ("Social and Behavioral Sciences", "SBS"),
    #     ("Civil Engineering", "CE"),
    #     ("School of Design and Construction", "SDC"),
    #     ("Human Resources", "HR"),
    #     ("Libraries", "Lib"),
    #     ("CEREO and the School of the Environment", "CEREO/SoE"),
    #     ("AgWeatherNet", "AWN"),
    #     ("College of Medicine", "CoM"),
    #     ("English", "Eng"),
    #     ("Nursing", "Nurs"),
    #     ("Crop and Soil Sciences", "CSS"),
    #     ("Community, Environment and Development", "CED"),
    #     ("Mechanical and Materials Engineering", "MME"),
    #     ("Social Sciences", "SS"),
    #     ("School of Biological Sciences", "SBS"),
    #     ("Animal Science", "AS"),
    #     ("Extension - Agriculture and Natural Resources", "E-ANR"),
    #     ("Global Animal Health", "GAH"),
    #     ("Institute of Biological Chemistry", "IBC"),
    #     ("Plant Pathology", "PP"),
    #     ("Electrical Engineering", "EE"),
    #     ("Arts and Sciences", "A&S"),
    #     ("Politics, Philosophy, and Public Affairs", "PPPA"),
    #     ("Institute of Biological Chemistry", "IBC"),
    #     ("College of Arts and Sciences, School of the Environment", "CAS/SoE"),
    #     ("WSU Press", "Press"),
    #     ("Geology", "Geo"),
    #     ("Landscape Architecture", "LA"),
    #     ("Sociology", "Soc"),
    #     ("Hospitality Business Management", "HBM"),
    #     ("Division of Governmental Studies and Services", "DGSS"),
    #     ("Integrative Physiology and Neuroscience", "IPN"),
    #     ("Civil and Environmental Engineering", "CEE"),
    #     ("Civil & Environmental Engineering", "CEE"),
    #     ("Washington Stormwater Center", "WSC"),
    #     ("Natural Resources", "NR"),
    #     ("Chemical", "Chem"),
    #     ("Earth Sciences", "ES"),
    #     ("School Of Biological Sciences", "SBS"),
    #     ("Communications", "Comm"),
    #     ("Mathematics and Statistics", "Math/Stat"),
    #     ("School of Economic Sciences", "SES"),
    #     ("College of Arts and Sciences", "CAS"),
    #     ("Biological Systems Engineering", "BSE"),
    #     ("Pre-Law Resource Center", "PLRC"),
    #     ("Horticulture", "Hort"),
    #     ("Extension Ag and Natural Resources Unit", "E-ANRU"),
    #     ("Extension", "Ext"),
    #     ("Division of Global Research and Engagement", "DGRE"),
    #     ("Office of Equity and Diversity", "OED"),
    #     ("Center for Sustaining Agriculture and Natural Resources", "CSANR"),
    #     ("College of Education", "CoE"),
    #     ("Water Research Center", "WRC"),
    #     ("Entomology", "Ento"),
    #     ("Voiland School of Chemical Engineering and Bioengineering", "VSCEB"),
    #     ("CIVIL AND ENVIRONMENTAL ENGINEERING", "CEE"),
    #     ("Microbiology/EECS", "Micro/EECS"),
    #     ("Extension - ANR Prog Unit", "Ext-ANRPU"),
    #     ("Pharmaceutical Sciences", "PharmSci"),
    #     ("School of Education", "SOE"),
    #     ("Global Politics", "GP"),
    #     ("CEE LAR", "CEE LAR"),
    #     ("DEPARTMENT OF CIVIL AND ENVIRONMENTAL ENGINEERING", "CEE"),
    #     ("LAR", "LAR"),
    #     ("Civil and Environmental engineering", "CEE"),
    #     ("Economics", "Econ"),
    #     ("Laboratory for Atmospheric Research", "LAR"),
    #     ("HONORS COLLEGE", "HC"),
    #     ("School of Engineering", "SoE"),
    #     ("Fine Arts", "FA"),
    #     ("School of Mechanical and Materials Engineering", "SMME"),
    #     ("Communications", "Comm"),
    #     ("Environmental Science", "EnvSci"),
    #     ("Center for Institutional Studies and Enrollment", "CISER"),
    #     ("Any", "Any"),
    #     ("Communication", "Comm"),
    #     ("Criminal Justice and Criminology", "CJC"),
    #     ("Civil and Environmental", "CEE"),
    #     ("Nursing", "Nurs"),
    #     ("WSU Extension - Ag. and Natural Resources Prog. Unit", "WSUE-ANRPU"),
    #     ("Edward R. Murrow College of Communication", "ERMCOC"),
    #     ("Corporate and Foundation Relations", "CFR"),
    #     ("Chemistry", "Chem"),
    #     ("Mathematics", "Math"),
    #     ("Crops and Soils", "C&S"),
    #     ("Admin/Washington Stormwater Center", "Admin/WSC"),
    #     ("Civil", "CEE"),
    #     ("Environmental and Natural Resource Sciences", "ENRS"),
    #     ("Crop and Soil Science", "CSS"),
    #     ("Apparel, Merchandising, Design and Textiles", "AMDT"),
    #     ("None", "None"),
    #     ("Crop and Soil Sciences", "CSS"),
    #     ("Cultural Studies and Social Thought in Education", "CSSTE"),
    #     ("Electrical Engineering and Computer Science", "EECS"),
    #     ("History", "Hist"),
    #     ("CEREO & WRC", "CEREO/WRC"),
    #     ("Ucomm", "Ucomm")
    # ]
#
    # allI = Department.query.all()

    # temp = []
    # for interest_test in allI:
    #     interest_name = interest_test.name
    #     temp.append(interest_name)

    # unique_abbr = set()  # Use set to ensure unique abbreviations
#
    # for x in checkList:
    #     for value in x:
    #         if value in temp:
    #             unique_abbr.add(x[1])  # Add the abbreviation to the set

    # # Convert the set of unique abbreviations to a sorted list
    # sorted_abbr = sorted(list(unique_abbr))

    # response = {
    #     "data": sorted_abbr
    # }

    # return jsonify(sorted_abbr)


# Assuming you have the current user available in your route context


@routes_blueprint.route('/user_interests')
def user_interests():
    if current_user.is_authenticated:
        user_interests = current_user.interests
        combined_data = {}

        for interest in user_interests:
            interest_name = interest.name
            subcategory_name = interest.subcategory.name if interest.subcategory else None

            if interest_name not in combined_data:
                combined_data[interest_name] = {
                    "Interest": interest_name, "SubCategories": []}

            if subcategory_name:
                combined_data[interest_name]["SubCategories"].append(
                    subcategory_name)

        result_data = list(combined_data.values())

        return jsonify({
            current_user.email: result_data
        })

    return "User not found or not logged in"


# pip install google-search-results

def parseData():
    # Read the data from the file
    with open('serpApi.txt', 'r') as file:
        data = file.read()

    # Remove the outer brackets to obtain individual publications
    publications_text = data.strip('[]')

    # Split the text to get individual publications
    publications = publications_text.split('},{')

    # Clean up the data (remove curly braces, etc.)
    cleaned_publications = [pub.strip('{}') for pub in publications]

    # Process or print each individual publication's details
    for pub in cleaned_publications:
        i = 0
        if (i == 0):
            # You can save this to another file or perform further parsing as needed
            print(pub)
            i = i+1




from flask import request


@routes_blueprint.route('/select_values', methods=['GET', 'POST'])
def select_values():
    form = Edit()

    form.set_air_choices()
    form.set_water_choices()

    if request.method == 'POST':
        selected_table = request.form.get('selected_table')
        selected_value = request.form.get('selected_value')

        if form.validate_on_submit():
            if selected_table == 'Air':
                air_instance = Air(name=selected_value)
                db.session.add(air_instance)
                db.session.commit()
                return "Value saved to Air model"
            elif selected_table == 'Water':
                water_instance = Water(name=selected_value)
                db.session.add(water_instance)
                db.session.commit()
                return "Value saved to Water model"
            else:
                return "Unexpected selection"

    return render_template('dropdowns.html', form=form)



############SAD BOI@routes_blueprint.route('/edit_interest', methods=['GET', 'POST'])
@routes_blueprint.route('/edit_interest', methods=['GET', 'POST'])
def edit_interest():
    form = EditInterest()
    eform = EditInterestSmall()

    # Populate the dropdown choices
    form.set_name()
    eform.set_name_small()

    selected_big_interest = None
    selected_small_interest = None

    if form.validate_on_submit():
        # Get the selected interest name from the big interest form
        selected_interest = form.name.data

        if selected_interest:  # Check if not blank
            print(f"Selected Big Interest: {selected_interest}")

            # Create a new BigInterest instance with the selected interest name
            new_interest = BigInterest(name=selected_interest, affiliate_id=current_user.id)

            # Add the new interest to the database
            db.session.add(new_interest)
            db.session.commit()

            selected_big_interest = selected_interest

            # Call set_name again to update choices with the new interest
            form.set_name()

    elif eform.validate_on_submit():
        # Get the selected interest name from the small interest form
        selected_interest_small = eform.name.data

        if selected_interest_small:  # Check if not blank
            print(f"Selected Small Interest: {selected_interest_small}")

            # Create a new smallInterest instance with the selected interest name
            new_interest_small = smallInterest(name=selected_interest_small, affiliate_id=current_user.id)

            # Add the new small interest to the database
            db.session.add(new_interest_small)
            db.session.commit()

            selected_small_interest = selected_interest_small

            # Call set_name_small again to update choices with the new interest
            eform.set_name_small()

 


        return render_template('edit_interest.html', form=form, eform=eform, selected_big_interest=selected_big_interest, selected_small_interest=selected_small_interest)

    return render_template('edit_interest.html', form=form, eform=eform, selected_big_interest=selected_big_interest, selected_small_interest=selected_small_interest)
    #return redirect(url_for("routes.index"))

@routes_blueprint.route('/delete_education/<user_id>/<education_id>', methods=['GET','POST'])
@login_required
def delete_education(education_id, user_id):
    education = Education.query.filter_by(id=education_id).first()
    if int(user_id) == current_user.id or current_user.is_admin:
        db.session.delete(education)
        db.session.commit()
    else:
        flash("You are not authorized.")
        return redirect(url_for("routes.index"))
    flash("You have deleted {name}".format(name=education.title))
    if current_user.is_admin:
        return redirect(url_for("auth.admin_edit_profile", user_id=user_id))
    return redirect(url_for("routes.edit_profile"))

@routes_blueprint.route('/delete_experience/<user_id>/<experience_id>', methods=['GET','POST'])
@login_required
def delete_experience(experience_id, user_id):
    experience = Experience.query.filter_by(id=experience_id).first()
    if int(user_id) == current_user.id or current_user.is_admin:
        db.session.delete(experience)
        db.session.commit()
    else:
        flash("You are not authorized.")
        return redirect(url_for("routes.index"))

    flash("You have deleted {name}".format(name=experience.title))
    if current_user.is_admin:
        return redirect(url_for("auth.admin_edit_profile", user_id=user_id))
    return redirect(url_for("routes.edit_profile"))

@routes_blueprint.route('/delete_project/<user_id>/<project_id>', methods=['GET','POST'])
@login_required
def delete_project(project_id, user_id):
    project = Project.query.filter_by(id=project_id).first()
    if int(user_id) == current_user.id or current_user.is_admin:
        db.session.delete(project)
        db.session.commit()
    else:
        flash("You are not authorized.")
        return redirect(url_for("routes.index"))

    flash("You have deleted {name}".format(name=project.name))
    if current_user.is_admin:
        return redirect(url_for("auth.admin_edit_profile", user_id=user_id))
    return redirect(url_for("routes.edit_profile"))
