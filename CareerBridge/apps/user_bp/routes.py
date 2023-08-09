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


@blueprint.route('/sign_in', methods=['GET', 'POST'])
@login_required
def sign_in():
    form = LoginForm(request.form)
    return render_template('/accounts/login.html', form=form)




@blueprint.route('/team')
@login_required
def team():
    # Retrieve job listings from the database
    return render_template('/user/team.html')



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
