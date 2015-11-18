# -*- coding: utf-8 -*-

from app import db
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import INET


__author__ = 'ruipacheco'
__version__ = '0.1'


class Topic(db.Model):
    """
    Represents a topic.
    """

    __tablename__ = 'Topic'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64), nullable=False)
    first_post_id = db.Column(db.Integer, db.ForeignKey('Post.id'), nullable=False)
    first_post = db.relationship('Post', foreign_keys=[first_post_id])
    posts = db.relationship('Post')

    # def __repr__(self):
    #     return u"<%s 'id': %i, 'subject':%s, 'first_post_id':%s>" % (self.__class__.__name__, self.id, self.subject,
    #                                                                  self.first_post_id)


class Post(db.Model):
    """
    Represents a post.
    """

    __tablename__ = 'Post'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    name = db.Column(db.String(64))
    email = db.Column(EmailType)
    ip_address = db.Column(INET, nullable=False)

    def __repr__(self):
        return u"<%s 'id': %i, 'topic_id':%i, 'message':%s, 'name':%s, 'email':%s, 'ip_address':%s>" % \
               (self.__class__.__name__, self.id, self.topic_id, self.message, self.name, self.email, self.ip_address)
