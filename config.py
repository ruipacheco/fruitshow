# -*- coding: utf-8 -*-


__author__ = 'ruipacheco'
__version__ = '0.1'


# Forum configuration
class ForumConfiguration(object):
    """
    Class used to cluster forum properties.
    """
    MAX_POSTS_INDEX_PAGE = 100
    FORUM_NAME = 'Fruitshow'

# Change when deploying to production
SECRET_KEY = u"\xefD\nj\xa7\xb3'\xc1\x9e\xef&\x13\xe7\xdf\xe0\xab\xe6\xac\x16\x84\xe60\x81v"
DEBUG = False
SQLALCHEMY_ECHO = False
WTF_CSRF_ENABLED = False
SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://fruitshow:fruitshow@localhost:5432/fruitshow'

# Don't change
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
