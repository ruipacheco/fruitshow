# -*- coding: utf-8 -*-

from app import db
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy_utils import EmailType

__author__ = 'ruipacheco'
__version__ = '0.1'


class Topic(db.Model):
    """
    Represents a topic.
    """

    __tablename__ = 'Topic'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64), nullable=False)
    first_post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))
    first_post = db.relationship('Post', foreign_keys=[first_post_id])


class Post(db.Model):
    """
    Represents a post.
    """

    __tablename__ = 'Post'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    topic = db.relationship('Topic', backref='posts', primaryjoin=topic_id == Topic.id, post_update=True)
    message = db.Column(db.String, nullable=False)
    name = db.Column(db.String(64))
    email = db.Column(EmailType)
    ip_address = db.Column(INET, nullable=False)
