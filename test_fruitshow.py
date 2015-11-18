# -*- coding: utf-8 -*-

"""
Functional and unit tests.
"""
from abc import ABCMeta

import pytest
from app import flask
from app.models import *
from pyquery import PyQuery


__author__ = 'ruipacheco'
__version__ = '0.1'


@pytest.fixture
def client(request):
    """
    Creates an instance of the web application.
    :return:
    """
    flask.config['TESTING'] = True
    a_client = flask.test_client()
    return a_client


@pytest.mark.usefixtures("client")
class AbstractTest(object):
    __metaclass__ = ABCMeta

    def get_element(self, html, element):
        parsed_html = PyQuery(html)
        element = parsed_html(element)
        return element

    def check_element_with_attrs(self, html, element, attributes={}):
        """
        This method uses PyQuery to find an element in a web page. It's possible to use css selectors to find the
        element.

        :param html: The HTML document to parse.
        :type html: str
        :param element: The element to look for in the document. May include class and id.
        :type element: str
        :param attributes: Holds the name:value of attributes to find in the element.
        :type attributes: {}
        """
        element = self.get_element(html, element)
        if 'class' in attributes:
            assert element.filter('.' + attributes['class'])
            del attributes['class']
        for key in attributes.keys():
            assert element.attr(key) == attributes[key]


class TestFunctional(AbstractTest):

    @classmethod
    def setup_class(cls):
        for i in range(0, 200):
            topic = Topic(subject=u'Topic %i' % i)
            for j in range(0, 5):
                post = Post(message=u'This is message %i' % j, topic_id=topic.id, ip_address=u'127.0.0.1')
                if not topic.first_post_id:
                    topic.first_post_id = post.id
                topic.posts.append(post)
            db.session.add(topic)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        db.session.execute('truncate "Topic" cascade')
        db.session.commit()

    def test_create_topic(self, client):
        pass
