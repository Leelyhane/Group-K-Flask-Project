# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, DateTimeField
from wtforms.validators import Email, DataRequired

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
    job_type = TextField(validators=[DataRequired()])
    company = TextField(validators=[DataRequired()])
    location = TextField(validators=[DataRequired()])
    description = TextField(validators=[DataRequired()])
    application_deadline = DateTimeField(
        validators=[DataRequired()], format='%Y-%m-%dT%H:%M')


class Internships(FlaskForm):
    job_name = TextField(validators=[DataRequired()])
    job_type = TextField(validators=[DataRequired()])
    company = TextField(validators=[DataRequired()])
    location = TextField(validators=[DataRequired()])
    description = TextField(validators=[DataRequired()])
    application_deadline = DateTimeField(
        validators=[DataRequired()], format='%Y-%m-%dT%H:%M')


class SubmitJobResume(FlaskForm):
    name = TextField(validators=[DataRequired()])
    email = TextField(validators=[DataRequired(), Email()])
    resume_file = TextField(validators=[DataRequired()])


class SubmitInternResume(FlaskForm):
    name = TextField(validators=[DataRequired()])
    email = TextField(validators=[DataRequired(), Email()])
    resume_file = TextField(validators=[DataRequired()])
