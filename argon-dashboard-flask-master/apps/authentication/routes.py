# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, render_template, request, redirect, url_for
from forms import SubmitJobResume
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
from apps.authentication.models import Users, Job_listings

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            if user.is_admin == True:
                return render_template('/home/index.html',)
            else:
                return render_template('index.html')

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


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


@blueprint.route('/add-job')
def add_job():
    # create_job_form = JobListings(request.form)
    if request.method == "POST":
        if 'job_name' in request.form and 'company_name' in request.form and 'job_description' in request.form and 'job-type' in request.form and 'application_deadline' in request.form:
            # Get the form data submitted by the admin
            job_name = request.form['job_name']
            company_name = request.form['company_name']
            job_description = request.form['job_description']
            job_category = request.form['job_type']
            application_deadline = request.form['application_deadline']

            # Convert Date Strings to Python date objects
            from datetime import datetime
            deadline = datetime.strptime(
                application_deadline, '%Y-%m-%').date()

            # Insert the job listing details into the database
            job = Job_listings(**request.form)
            db.session.add(job)
            db.session.commit()

            # Redirect to the available jobs page after successful submission
            return render_template('/home/available-jobs.html')

        # For GET requests, render the add_job.html template with an empty form
    return render_template('/home/add-job.html')


@blueprint.route('/add-intern', methods=['POST'])
def add_intern():
    if request.method == "POST":
        if 'job_name' in request.form and 'company_name' in request.form and 'job_description' in request.form and 'job_type' in request.form and 'application_deadline' in request.form:
            # Get the form data submitted by the admin
            job_name = request.form['job_name']
            company_name = request.form['company_name']
            job_description = request.form['job_description']
            job_category = request.form['job_type']
            application_deadline = request.form['application_deadline']

            # Convert Date Strings to Python date objects
            from datetime import datetime
            deadline = datetime.strptime(
                application_deadline, '%Y-%m-%d').date()

            # Insert the intern listing details into the database
            intern = Internships(**request.form)
            db.session.add(intern)
            db.session.commit()

            # Redirect to the available internships page after successful submission
            return redirect(url_for('/home/available-internships.html'))

    # For GET requests, render the add_intern.html template with an empty form
    return render_template('home/add-intern.html')


@blueprint.route('/submit-job-resume', methods=['GET', 'POST'])
def submit_job_resume():
    form = SubmitJobResume()

    if form.validate_on_submit():
        # If the form is successfully submitted and validated, you can process the data here
        name = form.name.data
        email = form.email.data
        resume_file = form.resume_file.data

        # Add your code to process the resume submission here

        # Redirect to a confirmation page after successful submission
        return redirect(url_for('job_resume_submission_confirmation'))

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    return render_template('submit-job-resume.html', form=form)


@blueprint.route('/submit-intern-resume', methods=['GET', 'POST'])
def submit_job_resume():
    form = SubmitInternResume()

    if form.validate_on_submit():
        # If the form is successfully submitted and validated, you can process the data here
        name = form.name.data
        email = form.email.data
        resume_file = form.resume_file.data

        # Add your code to process the resume submission here

        # Redirect to a confirmation page after successful submission
        return redirect(url_for('intern_resume_submission_confirmation'))

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    return render_template('submit-intern-resume.html', form=form)


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


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
