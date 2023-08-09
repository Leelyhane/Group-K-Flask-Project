# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from base64 import b64encode
from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from functools import wraps
from werkzeug.utils import secure_filename
import os

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, JobListings, Internship, SubmitInternResume, SubmitJobResume
from apps.authentication.models import Users, Job_listings, Internships, Job_resumes, Intern_resumes
# Import the 'home_blueprint' instance
from apps.home import blueprint as home_blueprint
from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return render_template('user/indexx.html')

# Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():

        # read form data
        username = login_form.username.data
        password = login_form.password.data

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password using a secure method, for example, bcrypt
        if user and verify_password(password, user.password):
            login_user(user)

            if user.is_admin:
                return redirect(url_for('home_blueprint.index'))
            else:
                return render_template('user/index1.html')

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)

    return render_template('accounts/login.html', form=login_form)


def verify_password(password, hashed_password):
    # Implement a secure password verification mechanism, for example, bcrypt
    # Compare the hashed password stored in the database with the provided password
    return True  # Replace this with the actual password verification implementation


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/add-job', methods=['POST', 'GET'])
def add_job():

    if request.method == "POST":
        job_name = request.form.get('job_name')
        company_name = request.form.get('company')
        job_description = request.form.get('description')
        job_category = request.form.get('job_category')
        location = request.form.get('location')
        application_deadline = request.form.get('application_deadline')
        company_logo = request.files.get('company_logo')
        company_url = request.form.get('company_url')

        if not job_name or not company_name or not job_description or not job_category:
            return "Error: Please fill in all required fields.", 400

        company_logo_data = company_logo.read() if company_logo else None
        company_logo_base64 = None

        if company_logo_data:
            company_logo_base64 = b64encode(company_logo_data).decode('utf-8')

      # Convert Date Strings to Python date objects
        from datetime import datetime
        try:
            deadline = datetime.strptime(
                application_deadline, '%Y-%m-%d').date()
        except ValueError:
            return "Error: Invalid date format for application deadline.", 400

            # Insert the job listing details into the database
        job_listing = Job_listings(
            job_name=job_name,
            company=company_name,
            desription=job_description,
            location=location,
            job_type=job_category,
            application_deadline=deadline,
            company_logo=company_logo_base64,
            company_url=company_url
        )

        db.session.add(job_listing)
        db.session.commit()
        print("Data added successfully.")
        # Redirect to the available jobs page after successful submission
        segment = 'available-jobs'
        field = ["COMPANY", "JOB", "CATEGORY", "DEADLINE"]
        job_listings = Job_listings.query.all()
        return render_template('/home/available-jobs.html', segment=segment, field=field, job_listings=job_listings)

    segment = 'add-job'

    # For GET requests or invalid form submissions, render the add_job.html template with the form
    return render_template('/home/add-job.html', segment=segment)


@blueprint.route('/remove-job/<int:job_id>',  methods=['GET', 'POST'])
def delete_job(job_id):
    job_listing = Job_listings.query.get(job_id)
    if job_listing:
        db.session.delete(job_listing)
        db.session.commit()
    return redirect(request.referrer)


@blueprint.route('/add-intern', methods=['POST', 'GET'])
def add_intern():

    if request.method == "POST":
        intern_name = request.form.get('intern_name')
        company_name = request.form.get('company')
        internship_description = request.form.get('description')
        job_category = request.form.get('job_category')
        location = request.form.get('location')
        application_deadline = request.form.get('application_deadline')
        company_logo = request.files.get('company_logo')
        company_url = request.form.get('company_url')

        if not intern_name or not company_name or not internship_description or not job_category:
            return "Error: Please fill in all required fields.", 400

        company_logo_data = company_logo.read() if company_logo else None
        company_logo_base64 = None

        if company_logo_data:
            company_logo_base64 = b64encode(company_logo_data).decode('utf-8')

      # Convert Date Strings to Python date objects
        from datetime import datetime
        try:
            deadline = datetime.strptime(
                application_deadline, '%Y-%m-%d').date()
        except ValueError:
            return "Error: Invalid date format for application deadline.", 400

            # Insert the job listing details into the database
        internship = Internships(
            intern_name=intern_name,
            company=company_name,
            description=internship_description,
            locaion=location,
            job_type=job_category,
            application_deadline=deadline,
            company_logo=company_logo_base64,
            company_url=company_url
        )

        db.session.add(internship)
        db.session.commit()
        print("Data added successfully.")
        # Redirect to the available jobs page after successful submission
        segment = 'available-internships'
        field = ["COMPANY", "INTERNSHIP", "CATEGORY", "DEADLINE"]
        internships = Internships.query.all()
        return render_template('/home/available-internships.html', segment=segment, field=field, internships=internships)

    segment = 'add-intern'

    # For GET requests or invalid form submissions, render the add_job.html template with the form
    return render_template('/home/add-intern.html', segment=segment)

# Remove Internships from the list of available internships
@blueprint.route('/remove-intern/<int:intern_id>',  methods=['GET', 'POST'])
def delete_intern(intern_id):
    intern = Internships.query.get(intern_id)
    if intern:
        db.session.delete(intern)
        db.session.commit()
    return redirect(request.referrer)

# Submitting a Job Resume.

#Handling PDF Files
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    return file.content_length <= MAX_FILE_SIZE

@blueprint.route('/submit_resume_job', methods=['GET', 'POST'])
def submit_job_resume():

    if request.method == 'POST':
        print("Received form data:", request.form)
        # If the form is successfully submitted and validated, you can process the data here
        job_id = request.form.get('job_id')
        name = request.form.get('name')
        email = request.form.get('email')
        resume_file = request.files.get('resume_file')

        
        if not job_id or not name or not email or not resume_file:
            flash('Please fill in all required fields.')
            return redirect(request.referrer)  # Redirect back to the previous page

        if 'resume_file' not in request.files or resume_file.filename == '':
            return 'No file selected', 400
        
        if not os.path.exists('uploads'):
           os.makedirs('uploads')

        if resume_file and allowed_file(resume_file.filename) and validate_file_size(resume_file):
            filename = secure_filename(resume_file.filename)
            resume_file.save(os.path.join('uploads', filename)) 
             
            job_resume = Job_resumes(
                job_id=job_id,
                name=name, email=email, resume_file=filename
            )
            db.session.add(job_resume)
            db.session.commit()
            flash('success')
            return render_template('/user/index1.html', flash=flash) 
        
        flash('Application Sent Successfully')
        # Redirect to a confirmation page after successful submission
        return render_template('/user/index1.html', flash=flash)

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form

    return render_template('/user/jobs.html')

# Submitting Intern Applications
@blueprint.route('/submit_resume_intern', methods=['GET', 'POST'])
def submit_intern_resume():

    if request.method == 'POST':
        print("Received form data:", request.form)
        # If the form is successfully submitted and validated, you can process the data here
        intern_id = request.form.get('intern_id')
        name = request.form.get('name')
        email = request.form.get('email')
        resume_file = request.files.get('resume_file')

        
        if not intern_id or not name or not email or not resume_file:
            flash('Please fill in all required fields.')
            return redirect(request.referrer)  # Redirect back to the previous page

        if 'resume_file' not in request.files or resume_file.filename == '':
            return 'No file selected', 400
        
        if not os.path.exists('uploads'):
           os.makedirs('uploads')

        if resume_file and allowed_file(resume_file.filename) and validate_file_size(resume_file):
            filename = secure_filename(resume_file.filename)
            resume_file.save(os.path.join('uploads', filename)) 
             
            intern_resume = Intern_resumes(
                intern_id=intern_id,
                name=name, email=email, resume_file=filename
            )
            db.session.add(intern_resume)
            db.session.commit()
            flash('success')
            return render_template('/user/index1.html', flash=flash) 
        
        flash('Application Sent Successfully')
        # Redirect to a confirmation page after successful submission
        return render_template('/user/index1.html', flash=flash)

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form

    return render_template('/user/jobs.html')

@blueprint.route('/job-resumes')
def submitted_job_resume():
 
    job_resume = Job_resumes.query.all()

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    segment = 'job-resumes'
    fields = ["JOB_ID", "APPLICANT NAME", "EMAIL", "RESUME FILE"]
    return render_template('/home/job-resumes.html', segment=segment, fields=fields, job_resume = job_resume)

# Displaying table of Submitted Internship Applications
@blueprint.route('/intern-resumes')
def submitted_intern_resume():
 
    intern_resume = Intern_resumes.query.all()

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    segment = 'intern-resumes'
    fields = ["INTERN_ID", "APPLICANT NAME", "EMAIL", "RESUME FILE"]
    return render_template('/home/intern-resumes.html', segment=segment, fields=fields, intern_resume = intern_resume)



# Users Routes

# Landing Page Route
@blueprint.route('/indexx')
def indexx():
    # Retrieve job listings from the database
    job_listings = Job_listings.query.all()
    internships = Internships.query.all()
    return render_template('/user/indexx.html', jobListings=job_listings, internships=internships)


@blueprint.route('/internships')
def internship():
    # Retrieve job listings from the database
    internships = Internships.query.all()
    print(internships)
    return render_template('/user/internships.html', internships=internships)

# Jobs Route.
@blueprint.route('/jobs')
def job():
    # Retrieve job listings from the database
    job_listings = Job_listings.query.all()
    return render_template('/user/jobs.html', jobListings=job_listings)

# Home page Route.
@blueprint.route('/index1')
def index1():
    # Retrieve job listings from the database
    job_listings = Job_listings.query.all()
    print(job_listings)
    return render_template('/user/index1.html', jobListings=job_listings)

#  Job Description Route.
@blueprint.route('/job-description/<int:job_id>')
def job_description(job_id):
    # Retrieve the specific job details from the database based on job_id
    job_details = Job_listings.query.get(job_id)
    return render_template('/user/job-description.html', job_details=job_details)

# Internship Description Route.
@blueprint.route('/intern-description/<int:intern_id>')
def intern_description(intern_id):
    # Retrieve the specific job details from the database based on job_id
    intern_details = Internships.query.get(intern_id)
    return render_template('/user/intern-description.html', intern_details=intern_details)

# Job Resume form submission Route.
@blueprint.route('/submit-job-resume/<int:job_id>')
def job_resume(job_id):
    # Retrieve the specific job details from the database based on job_id
    job_details = Job_listings.query.get(job_id)
    return render_template('/user/submit_job_resume.html', job_details=job_details)

# Internship Application form submission Route.
@blueprint.route('/submit-intern-resume/<int:intern_id>')
def intern_resume(intern_id):
    # Retrieve the specific job details from the database based on job_id
    intern_details = Internships.query.get(intern_id)
    return render_template('/user/submit_intern_resume.html', intern_details=intern_details)

# Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


# @blueprint.errorhandler(500)
# def internal_error(error):
#     return render_template('home/page-500.html'), 500
