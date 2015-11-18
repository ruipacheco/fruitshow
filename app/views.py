# -*- coding: utf-8 -*-

from app import flask, db
from flask import render_template

__author__ = 'ruipacheco'
__version__ = '0.1'


@flask.route('/')
def index():
    return render_template('index.html')
