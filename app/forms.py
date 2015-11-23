# -*- coding: utf-8 -*-

from flask_wtf import Form
from models import Post
from wtforms.fields import StringField, BooleanField
from wtforms.validators import InputRequired, Email, Optional
from wtforms.widgets.core import TextArea, TextInput
from wtforms_alchemy import ModelForm

__author__ = 'ruipacheco'
__version__ = '0.1'


class TopicForm(Form):
    """
    Form used to create a new topic. It includes the subject which is part of the Topic model and the message which is
    part of the first Post
    """
    subject = StringField(u'Subject:', validators=[InputRequired()])
    message = StringField(u'Message:', validators=[InputRequired()], widget=TextArea())
    name = StringField(u'Full name:')
    email = StringField(u'Email:', validators=[Optional(), Email()])
    remember_me = BooleanField(u'Remember me', default=True)

    def __repr__(self):
        return u"<%s 'subject':%s, 'email': %s, 'name': %s, 'message': %i>" \
               % (self.__class__.__name__, self.subject, self.email, self.name, self.message)


class PostForm(ModelForm):
    """
    Form used to create a new Post.
    """
    class Meta:
        model = Post
        only = [u'message', u'name', u'email']
        field_args = {u'name': {'widget': TextInput()}, }

    def __repr__(self):
        return u"<%s 'message': %s, 'name': %s, 'email': %s>" % self.message, self.name, self.email
