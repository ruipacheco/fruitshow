# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


__author__ = 'ruipacheco'
__version__ = '0.1'


flask = Flask(__name__)
flask.config.from_object('config')
db = SQLAlchemy(flask)

from app import forms, models, views
