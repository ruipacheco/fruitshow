# -*- coding: utf-8 -*-

import time
from urlparse import urlparse

from app import flask
from flask import render_template, abort, request, redirect, url_for
from forms import TopicForm, PostForm
from models import *
from sqlalchemy import func, distinct

__author__ = 'ruipacheco'
__version__ = '0.1'


def latest_visible_topics():
    """
    Returns a list with the latest visible topics.
    :return: [Topic]
    """
    topics = Topic.query.order_by(Topic.date_created).limit(100).all()
    return topics


@flask.route('/rss')
def rss():
    """
    Creates an RSS feed with all the items in the homepage.
    """
    form = {
        'title': 'Fruitshow',
        'hostname': urlparse(request.url_root).hostname,
        'time': time.strftime("%Y/%m/%d %H:%M:%S"),
        'description': 'Fruitshow'
    }
    topics = latest_visible_topics()
    return render_template('rss.txt', topics=topics, form=form)


@flask.route('/')
def index():
    """
    Home page of the forum. Displays the first 100 topics ordered by creation date.
    """
    topics = latest_visible_topics()
    return render_template('index.html', topics=topics)


@flask.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
def view_topic(topic_id):
    """
    Displays a Topic with all its posts.
    :param topic_id:
    :type topic_id: int
    """
    topic = Topic.query.filter_by(id=topic_id).first()
    if not topic:
        abort(404)
    form = PostForm(request.form)
    if request.method == 'POST':
        if form.validate():
            post = Post(message=form.message.data, ip_address=request.remote_addr, name=form.name.data,
                        email=form.email.data)
            post.topic = topic
            db.session.commit()
        return redirect(url_for('view_topic', topic_id=topic_id))
    return render_template('topic.html', topic=topic, form=form)


@flask.route('/topic/new', methods=['GET', 'POST'])
def new_topic():
    """
    Starts a new thread creating a new Topic and corresponding first Post in the database.
    """
    form = TopicForm(request.form)
    if form.validate_on_submit():
        topic = Topic(subject=form.subject.data)
        post = Post(message=form.message.data, ip_address=request.remote_addr, name=form.name.data,
                    email=form.email.data)
        topic.first_post = post
        post.topic = topic
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('view_topic', topic_id=topic.id))
    return render_template('new_topic.html', form=form)


@flask.route('/archive/')
@flask.route('/archive/<int:year>')
@flask.route('/archive/<int:year>/<int:month>')
def archive(year=0, month=0):
    """
    Shows archived threads, meaning all threads sorted by year and month.
    If no year is passed, then a list of all the years for which we have archived topics is displayed.
    If a year is passed, a list of all the months for which there are archived topics is displayed.
    If a month is passed, we show all archived topics for that month.

    @todo Need to pass the timezone to the extract() function.

    :param year:
    :type year: int
    :param month:
    :type month: int
    """
    if year > 0 and month > 0:
        elements = Topic.query.filter(func.extract('YEAR', Topic.date_created) == year,
                                      func.extract('MONTH', Topic.date_created) == month).all()
    else:
        if year > 0 and month == 0:
            results = db.session.query(distinct(func.extract('MONTH', Topic.date_created))). \
                filter(func.extract('YEAR', Topic.date_created) == year).all()
        if year == 0 and month == 0:
            results = db.session.query(distinct(func.extract('YEAR', Topic.date_created))).all()
        elements = []
        for result in results:
            elements.append(int(result[0]))
    return render_template('archive.html', elements=elements, year=year, month=month)
