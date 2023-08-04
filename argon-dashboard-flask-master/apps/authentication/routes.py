from flask import Flask, render_template, request, redirect, url_for
from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from functools import wraps

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, JobListings, Internships, SubmitInternResume, SubmitJobResume
from apps.authentication.models import Users, Job_listings, Internships, Job_resumes, Intern_resumes

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
    form = JobListings(request.form)

    if request.method == "POST" and form.validate():
        # Get the form data submitted by the admin
        job_name = form.job_name.data
        company_name = form.company.data
        job_description = form.job_description.data
        job_category = form.job_category.data
        location = form.location.data
        application_deadline = form.application_deadline.data
        company_logo = form.company_logo.data
        company_url = form.company_url.data

        # Convert Date Strings to Python date objects
        from datetime import datetime
        deadline = datetime.strptime(application_deadline, '%Y-%m-%d').date()

        # Insert the job listing details into the database
        job_listing = Job_listings(
            job_name=job_name,
            company=company_name,
            description=job_description,
            location=location,
            job_type=job_category,
            application_deadline=deadline,
            company_logo=company_logo,
            company_url=company_url
        )
        db.session.add(job_listing)
        db.session.commit()

        # Redirect to the available jobs page after successful submission
        return redirect(url_for('home_blueprint.available-jobs'))

    segment = 'add-job'

    # For GET requests or invalid form submissions, render the add_job.html template with the form
    return render_template('/home/add-job.html', form=form, segment=segment)


@blueprint.route('/add-intern', methods=['POST', 'GET'])
def add_internship():
    form = Internships(request.form)

    if request.method == "POST" and form.validate():
        # Get the form data submitted by the admin
        job_name = form.intern_name.data
        company_name = form.company.data
        internship_description = form.internship_description.data
        job_category = form.job_category.data
        location = form.location.data
        application_deadline = form.application_deadline.data
        logo = form.company_logo.data
        url = form.company_url.data

        # Convert Date Strings to Python date objects
        from datetime import datetime
        deadline = datetime.strptime(application_deadline, '%Y-%m-%d').date()

        # Insert the internship details into the database
        internship = Internships(
            job_name=job_name,
            company_name=company_name,
            job_description=internship_description,
            job_type=job_category,
            locaion=location,
            application_deadline=deadline,
            company_logo=logo,
            company_url=url
        )
        db.session.add(internship)
        db.session.commit()

        # Redirect to the available internships page after successful submission
        return redirect(url_for('home_blueprint.available-internships'))

    segment = 'add-intern'

    # For GET requests or invalid form submissions, render the add_intern.html template with the form
    return render_template('/home/add-intern.html', form=form, segment=segment)


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

    segment = 'job-resumes'

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    return render_template('/home/job-resumes.html', form=form, segment=segment)


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
        return render_template('/home/available-jobs.html')

    segment = 'intern-resumes'

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    return render_template('/home/intern-resumes.html', form=form, segment=segment)

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
