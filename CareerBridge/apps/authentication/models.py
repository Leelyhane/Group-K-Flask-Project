# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask_login import UserMixin
from apps import db, login_manager
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from apps.authentication.util import hash_pass


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class Job_listings(db.Model, UserMixin):

    __tablename__ = 'Job_listings'

    job_id = db.Column(db.Integer, primary_key=True, unique=True)
    job_type = db.Column(db.String(64))
    job_name = db.Column(db.String(64))
    company = db.Column(db.String(64))
    company_logo = db.Column(db.String(255))
    location = db.Column(db.String(64))
    desription = db.Column(db.String(255))
    application_deadline = db.Column(db.DateTime())
    company_url = db.Column(db.String(255))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.job_name)


class Internships(db.Model, UserMixin):

    __tablename__ = 'Internships'

    intern_id = db.Column(db.Integer, primary_key=True, unique=True)
    job_type = db.Column(db.String(64))
    intern_name = db.Column(db.String(64))
    company = db.Column(db.String(64))
    company_logo = db.Column(db.String(255))
    locaion = db.Column(db.String(64))
    description = db.Column(db.String(255))
    application_deadline = db.Column(db.DateTime())
    company_url = db.Column(db.String(255))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.intern_name)


class Job_resumes(db.Model, UserMixin):

    __tablename__ = 'Job_resumes'

    resume_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    resume_file = db.Column(db.String(255))
    job_id = db.Column(db.Integer, ForeignKey('Job_listings.job_id'))
    resume = relationship('Job_listings', backref='Job_resumes', lazy=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

    def __repr__(self):
        return str(self.name)


class Intern_resumes(db.Model, UserMixin):

    __tablename__ = 'Intern_resumes'

    resume_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    resume_file = db.Column(db.String(255))
    intern_id = db.Column(db.Integer, ForeignKey('Internships.intern_id'))
    resume = relationship('Internships', backref='intern_resumes', lazy=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

    def __repr__(self):
        return str(self.name)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None