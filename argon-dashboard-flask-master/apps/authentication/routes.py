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

"""
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


@blueprint.route('/add-job', methods=['POST'])
def add_job():
    if request.method == "POST":
        form = JobListings(request.form)
        if form.validate():  # Make sure to validate the form
            # Get the form data submitted by the admin
            job_name = form.job_name.data
            company_name = form.company.data
            job_description = form.job_description.data
            job_category = form.job_category.data
            location = form.location.data
            application_deadline = form.application_deadline.data
            company_logo = form.company_logo.data  # Get the company_logo field data
            company_url = form.company_url.data    # Get the company_url field data

            # Convert Date Strings to Python date objects
            from datetime import datetime
            deadline = datetime.strptime(
                application_deadline, '%Y-%m-%d').date()

            # Insert the job listing details into the database
            job_listing = Job_listings(
                job_name=job_name,
                company=company_name,
                description=job_description,
                location=location,
                job_type=job_category,
                application_deadline=deadline,
                company_logo=company_logo,  # Add the company_logo data to the model
                company_url=company_url     # Add the company_url data to the model
            )
            db.session.add(job_listing)
            db.session.commit()

            # Redirect to the available jobs page after successful submission
            return redirect(url_for('home_blueprint.available_jobs'))

    # For GET requests or invalid form submissions, render the add_job.html template with the form
    return render_template('/home/add-job.html', form=JobListings())


@blueprint.route('/add-intern', methods=['POST'])
def add_internship():
    if request.method == "POST":
        form = Internships(request.form)
        if form.validate_on_submit():
            # Get the form data submitted by the admin
            job_name = form.intern_name.data
            company_name = form.company.data
            internship_description = form.internship_description.data
            job_category = form.job_category.data
            location = form.location.data
            application_deadline = form.application_deadline.data
            logo = form.company_logo.data  # Get the company_logo field data
            url = form.company_url.data    # Get the company_url field data

            # Convert Date Strings to Python date objects
            from datetime import datetime
            deadline = datetime.strptime(
                application_deadline, '%Y-%m-%d').date()

            # Insert the internship details into the database
            internship = Internships(
                job_name=job_name,
                company_name=company_name,
                job_description=internship_description,
                job_category=job_category,
                locaion=location,
                application_deadline=deadline,
                company_logo=logo,  # Add the company_logo data to the model
                company_url=url     # Add the company_url data to the model
            )
            db.session.add(internship)
            db.session.commit()

            # Redirect to the available jobs page after successful submission
            return redirect(url_for('home_blueprint.available_internships'))

    # For GET requests or invalid form submissions, render the add_job.html template with the form
    return render_template('/home/add-intern.html', form=Internships())


@blueprint.route('/submit-job-resume', methods=['GET', 'POST'])
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
        return render_template('/home/index.html')

    # For GET requests or invalid form submissions, render the submit_job_resume.html template with the form
    return render_template('submit-job-resume.html', form=form)


@blueprint.route('/submit-intern-resume', methods=['GET', 'POST'])
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
        return render_template('/home/index.html')

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
<<<<<<< HEAD

 """

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated User and Admin database
users = {
    'user1': {'username': 'user1', 'password': 'password1', 'is_admin': False},
    'user2': {'username': 'user2', 'password': 'password2', 'is_admin': False},
    'admin': {'username': 'admin', 'password': 'adminpassword', 'is_admin': True},
}

# User class for Flask-Login


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.username = users[user_id]['username']
        self.password = users[user_id]['password']
        self.is_admin = users[user_id]['is_admin']

# Function to load user from the database


def load_user(user_id):
    return User(user_id)


# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return load_user(user_id)

# Route for login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((u for u in users.values(
        ) if u['username'] == username and u['password'] == password), None)

        if user:
            user_id = username
            remember = request.form.get('remember', False)
            user_obj = load_user(user_id)
            login_user(user_obj, remember=remember)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

# Route for dashboard (requires login)


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return render_template('admin_dashboard.html')
    else:
        return render_template('user_dashboard.html')

# Route for logout


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
