# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import Users, Job_listings, Internships, Job_resumes, Intern_resumes


@blueprint.route('/available-jobs')
@login_required
def index():
    field = ["COMPANY", "JOB", "CATEGORY", "DEADLINE"]
    job_listings = Job_listings.query.all()
    return render_template('home/available-jobs.html', segment='available-jobs', field=field, job_listings=job_listings)


# @blueprint.route('/add-intern')
# @login_required
# def intern():
#     segment = 'add-intern'
#     return render_template('home/add-intern.html', segment=segment)


# @blueprint.route('/add-job')
# @login_required
# def job():
#     segment = 'add-job'
#     return render_template('home/add-job.html', segment=segment)


@blueprint.route('/available-internships')
@login_required
def intern_available():
    fields = ["COMPANY", "INTERNSIP", "CATEGORY", "DEADLINE"]
    segment = 'available-internships'
    internships = Internships.query.all()
    return render_template('home/available-internships.html', segment=segment, internships=internships, field=fields)


@blueprint.route('/job-resumes')
@login_required
def job_resume():
    field = ["JOB_ID", "APPLICANT NAME", "EMAIL", "RESUME FILE"]
    job_resume = Job_resumes.query.all()
    segment = 'job-resumes'
    return render_template('home/job-resumes.html', segment=segment, job_resume=job_resume, fields=field)


@blueprint.route('/intern-resumes')
@login_required
def intern_resume():
    columns = ["JOB_ID", "APPLICANT NAME", "EMAIL", "RESUME FILE"]
    intern_resume = Intern_resumes.query.all()
    return render_template('home/intern-resumes.html', segment='intern-resumes', intern_resume=intern_resume, fields=columns)


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
            segment = 'available-jobs'

        return segment

    except:
        return None
