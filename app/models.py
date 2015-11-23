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
    subject = db.Column(db.Text(64), nullable=False)
    first_post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))
    first_post = db.relationship('Post', foreign_keys=[first_post_id])
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return u"<%s 'id':%i, 'subject':%s, 'first_post_id':%i, 'date_created':%s>" % (self.__class__.__name__,
                                                                                       self.id, self.subject,
                                                                                       self.first_post_id,
                                                                                       self.date_created)


class Post(db.Model):
    """
    Represents a post.
    """

    __tablename__ = 'Post'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    topic = db.relationship('Topic', backref='posts', primaryjoin=topic_id == Topic.id, post_update=True)
    message = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text(64))
    email = db.Column(EmailType)
    ip_address = db.Column(INET, nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return u"<%s 'id':%i, 'topic_id':%i, 'message':%s, 'name':%s, 'email':%s, 'ip_address':%s, 'date_created':%s>" \
               % (self.__class__.__name__, self.id, self.topic_id, self.message, self.name, self.email, self.ip_address,
                  self.date_created)
