# -*- coding: utf-8 -*-

from models import Post
from flask_wtf import Form
from wtforms_alchemy import ModelForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired, Email, Optional
from wtforms.widgets.core import TextArea, TextInput


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

