# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from functools import wraps

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

    # if current_user.is_admin:
    #     return render_template('home/available-jobs.html')
    # else:
    #     return render_template('user/index1.html')

# Helper - Verify password securely (implement the appropriate function for password verification)


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
            company_logo=company_logo.read() if company_logo else None,
            company_url=company_url
        )

        db.session.add(job_listing)
        db.session.commit()
        print("Data added successfully.")
        # Redirect to the available jobs page after successful submission
        segment = 'available-jobs'
        field = ["COMPANY", "JOB", "CATEGORY", "DEADLINE"]
        job_listings = Job_listings.query.all()
        return render_template('/home/available-jobs.html', segment=segment, field= field, job_listings=job_listings)

    segment = 'add-job'

    # For GET requests or invalid form submissions, render the add_job.html template with the form
    return render_template('/home/add-job.html', segment=segment)


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
            company_logo=company_logo.read() if company_logo else None,
            company_url=company_url
        )

        db.session.add(internship)
        db.session.commit()
        print("Data added successfully.")
        # Redirect to the available jobs page after successful submission
        segment = 'available-internships'
        field = ["COMPANY", "INTERNSHIP", "CATEGORY", "DEADLINE"]
        internships = Internships.query.all()
        return render_template('/home/available-internships.html', segment=segment, field= field, internships= internships)

    segment = 'add-intern'

    # For GET requests or invalid form submissions, render the add_job.html template with the form
    return render_template('/home/add-intern.html', segment=segment)

@blueprint.route('/job-resumes', methods=['GET', 'POST'])
def submit_job_resume():
    form = SubmitJobResume()

    if form.validate_on_submit():
        # If the form is successfully submitted and validated, you can process the data here
        name = form.name.data
        email = form.email.data
        resume_file = form.resume_file.data

        # Create a new JobResume instance and save the data to the database
        job_resume = Job_resumes(
            name=name, email=email, resume_file=resume_file)
        db.session.add(job_resume)
        db.session.commit()

        # Redirect to a confirmation page after successful submission
        return render_template('/home/available-jobs.html')

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    segment = 'job-resumes'
    fields = ["JOB_ID", "APPLICANT NAME", "EMAIL", "RESUME FILE"]
    return render_template('/home/job-resumes.html', form=form, segment=segment, fields=fields)


@blueprint.route('/intern-resumes', methods=['GET', 'POST'])
def submit_intern_resume():
    form = SubmitInternResume()

    if form.validate_on_submit():
        # If the form is successfully submitted and validated, you can process the data here
        name = form.name.data
        email = form.email.data
        resume_file = form.resume_file.data

        # Create a new JobResume instance and save the data to the database
        job_resume = Intern_resumes(
            name=name, email=email, resume_file=resume_file)
        db.session.add(job_resume)
        db.session.commit()

        # Redirect to a confirmation page after successful submission
        return render_template('/home/available-jobs.html', flash='Internship Resumes')

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    segment = 'intern-resumes'
    fields = ["JOB_ID", "APPLICANT NAME", "EMAIL", "RESUME FILE"]
    return render_template('/home/intern-resumes.html', form=form, segment=segment, fields=fields)

# Users Routes

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

@blueprint.route('/jobs')
def job():
    # Retrieve job listings from the database
    job_listings = Job_listings.query.all()
    return render_template('/user/jobs.html', jobListings=job_listings)


@blueprint.route('/index1')
def index1():
    # Retrieve job listings from the database
    job_listings = Job_listings.query.all()
    print(job_listings)
    return render_template('/user/index1.html', jobListings=job_listings)

@blueprint.route('/job-description/<int:job_id>')
def description(job_id):
    # Retrieve the specific job details from the database based on job_id
    job_details = Job_listings.query.get(job_id)
    return render_template('/user/job-description.html', job_details=job_details)



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
