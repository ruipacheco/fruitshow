# -*- coding: utf-8 -*-

from app import flask
from models import *
from forms import TopicForm, PostForm
from flask import render_template, abort, request, redirect, url_for


__author__ = 'ruipacheco'
__version__ = '0.1'


@flask.route('/')
def index():
    """
    Home page of the forum. Prints topics in lists of 100, along with a search box and a link to create a new topic.
    """
    topics = Topic.query.order_by(Topic.date_created).limit(100).all()
    return render_template('index.html', topics=topics)


@flask.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
def view_topic(topic_id):
    """
    Displays a thread with all its posts.
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
        return redirect(url_for('view_topic', topic_id=topic.id))
    return render_template('topic.html', topic=topic, form=form)


@flask.route('/topic/new', methods=['GET', 'POST'])
def new_topic():
    """
    Starts a new thread creating a new Topic in the database.
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
