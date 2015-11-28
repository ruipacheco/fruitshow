# -*- coding: utf-8 -*-

"""
Functional and unit tests.
"""
import pytest
from abc import ABCMeta
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

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        db.session.execute('truncate "Topic" cascade')
        db.session.commit()

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


class TestGETFunctional(AbstractTest):

    @classmethod
    def setup_class(cls):
        cls.total_topics = 300
        for i in range(0, cls.total_topics):
            topic = Topic(subject=u'Topic %i' % i)
            post = Post(message=u'First Post!', ip_address=u'127.0.0.1', name=u'Poster %i' % i,
                        email=u'email%i@email' % i)
            topic.first_post = post
            post.topic = topic
            for j in range(1, 25):
                post = Post(message=u'Post %i' % j, ip_address=u'127.0.0.1', name=u'Poster %i' % j,
                            email=u'email%i@email' % j)
                post.topic = topic
            db.session.add(topic)
        db.session.commit()

    def test_index_page(self, client):
        result = client.get('/')
        assert result.status_code == 200
        lists = self.get_element(result.data, 'li.topic')
        assert len(lists) == 100

    def test_list_all_years_in_archive(self, client):
        result = client.get('/archive', follow_redirects=True, environ_base={'REMOTE_ADDR': '127.0.0.1'})
        link = self.get_element(result.data, 'a')[1]
        assert link.attrib['href'] == '/archive/2015'

    def test_list_all_months_in_archive_per_year(self, client):
        result = client.get('/archive/2015', follow_redirects=True, environ_base={'REMOTE_ADDR': '127.0.0.1'})
        link = self.get_element(result.data, 'a')[2]
        assert link.attrib['href'] == '/archive/2015/11'

    def test_list_topics_in_month_in_archive(self, client):
        result = client.get('/archive/2015/11', follow_redirects=True, environ_base={'REMOTE_ADDR': '127.0.0.1'})
        li = self.get_element(result.data, 'li.topic')
        assert len(li) == TestGETFunctional.total_topics


class TestPOSTFunctional(AbstractTest):

    def test_create_new_thread(self, client):
        data = {
            'subject': u'A subject',
            'message': u'A message',
            'name': u'A name'
        }
        result = client.post('/topic/new', follow_redirects=True, data=data, environ_base={'REMOTE_ADDR': '127.0.0.1'})
        assert result.status_code == 200
        article = self.get_element(result.data, 'article')[0]
        assert u'A message' in article.text

    def test_add_new_post_to_topic(self, client):
        data = {
            'subject': u'A subject',
            'message': u'A message',
            'name': u'A name'
        }
        result = client.post('/topic/new', follow_redirects=True, data=data, environ_base={'REMOTE_ADDR': '127.0.0.1'})
        assert result.status_code == 200
        h3 = self.get_element(result.data, 'h3')
        topic_id = h3.attr('id')
        data = {
            'message': u'A second message',
            'name': u'A second name'
        }
        result = client.post('/topic/%s' % topic_id, follow_redirects=True, data=data,
                             environ_base={'REMOTE_ADDR': '127.0.0.1'})
        assert result.status_code == 200
        article = self.get_element(result.data, 'article')[1]
        assert u'A second message' in article.text
