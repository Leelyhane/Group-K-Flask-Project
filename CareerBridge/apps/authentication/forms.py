# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, DateTimeField, TextAreaField, StringField
from wtforms.validators import Email, DataRequired, URL
from flask_wtf.file import FileField, FileAllowed, FileRequired

# login and registration

class LoginForm(FlaskForm):
    username = TextField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])


class JobListings(FlaskForm):
    job_name = TextField(validators=[DataRequired()])
    job_category = TextField(validators=[DataRequired()])
    company = TextField(validators=[DataRequired()])
    company_logo = FileField(validators=[
        # Limit allowed file types
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
        # Add more validators based on your specific criteria (e.g., FileSize, Dimensions, AspectRatio)
    ])
    location = TextField(validators=[DataRequired()])
    # URL validator for company URL
    company_url = StringField(validators=[URL()])
    job_description = TextAreaField(validators=[DataRequired()], render_kw={
        "class": "description"})  # Use TextAreaField for description
    application_deadline = DateTimeField(
        validators=[DataRequired()], format='%Y-%m-%dT%H:%M')


class Internship(FlaskForm):
    intern_name = TextField(validators=[DataRequired()])
    job_category = TextField(validators=[DataRequired()])
    company = TextField(validators=[DataRequired()])
    company_logo = FileField(validators=[
        # Ensure a file is uploaded
        # Limit allowed file types
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
        # Add more validators based on your specific criteria (e.g., FileSize, Dimensions, AspectRatio)
    ])
    location = TextField(validators=[DataRequired()])
    # URL validator for company URL
    company_url = StringField(validators=[URL()])
    internship_description = TextAreaField(validators=[DataRequired()], render_kw={
        "class": "description"})  # Use TextAreaField for description
    application_deadline = DateTimeField(
        validators=[DataRequired()], format='%Y-%m-%dT%H:%M')


class SubmitJobResume(FlaskForm):
    name = TextField(validators=[DataRequired()])
    email = TextField(validators=[DataRequired(), Email()])
    resume_file = FileField(validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])


class SubmitInternResume(FlaskForm):
    name = TextField(validators=[DataRequired()])
    email = TextField(validators=[DataRequired(), Email()])
    resume_file = FileField(validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
