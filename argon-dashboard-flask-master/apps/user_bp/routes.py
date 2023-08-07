# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.user_bp import blueprint
from apps.authentication import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.forms import LoginForm
from apps.authentication.models import Job_listings, Internships


# @blueprint.route('/indexx')
# def indexx():
#     # Retrieve job listings from the database
#     job_listings = Job_listings.query.all()
#     print(job_listings)
#     return render_template('/user/indexx.html', jobListings=job_listings)


@blueprint.route('/sign_in', methods=['GET', 'POST'])
@login_required
def sign_in():
    form = LoginForm(request.form)
    return render_template('/accounts/login.html', form=form)


# @blueprint.route('/index1')
# @login_required
# def index1():
#     # Retrieve job listings from the database
#     job_listings = Job_listings.query.all()
#     print(job_listings)
#     return render_template('/user/index1.html', jobListings=job_listings)


# @blueprint.route('/internships')
# @login_required
# def internship():
#     # Retrieve job listings from the database
#     internships = Internships.query.all()
#     print(internships)
#     return render_template('/user/internships.html', internships=internships)


# @blueprint.route('/jobs')
# @login_required
# def job():
#     # Retrieve job listings from the database
#     job_listings = Job_listings.query.all()
#     print(job_listings)
#     return render_template('/user/jobs.html', jobListings=job_listings)


@blueprint.route('/description')
@login_required
def description():
    # Retrieve job listings from the database
    job_listings = Job_listings.query.all()
    internships = Internships.query.all()
    print(job_listings)
    return render_template('/user/description.html', jobListings=job_listings, internships=internships)


@blueprint.route('/team')
@login_required
def team():
    # Retrieve job listings from the database
    return render_template('/user/team.html')


@blueprint.route('/contact')
@login_required
def contact():
    # Retrieve job listings from the database
    return render_template('/user/contact.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
