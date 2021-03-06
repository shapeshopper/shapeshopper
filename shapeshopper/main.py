#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


class SSuser(ndb.Model):
    first_name = ndb.StringProperty(default="")
    last_name = ndb.StringProperty(default="")
    email = ndb.StringProperty(default="")
    confirm_email = ndb.StringProperty(default="")
    password = ndb.StringProperty(default="")
    confirm_password = ndb.StringProperty(default="")
    birth_month = ndb.StringProperty(default="")
    birth_day = ndb.StringProperty(default="")
    image = ndb.StringProperty(default="")

class ListHandler(webapp2.RequestHandler):
    def get(self):
        data = {
            'admin': users.is_current_user_admin(),
            'user': users.get_current_user(),
            'login': users.create_login_url(dest_url=self.request.url),
            'logout': users.create_logout_url(dest_url=self.request.url),
        }
        template = env.get_template('friends.html')
        self.response.out.write(template.render(data))


env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('home.html')
        data = {
            'admin': users.is_current_user_admin(),
            'user': users.get_current_user(),
            'login': users.create_login_url(dest_url=self.request.url),
            'logout': users.create_logout_url(dest_url=self.request.url),
        }
        self.response.out.write(main_template.render(data))
    def post(self):
        survey_template = env.get_template('survey.html')

class SurveyHandler(webapp2.RequestHandler):
    def get(self):
        survey_template = env.get_template('survey.html')
        self.response.out.write(survey_template.render())

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        home_template = env.get_template('home.html')
        self.response.out.write(home_template.render())

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        result_template = env.get_template('results.html')

        height = int(self.request.get('height'))

        if height in range (59, 63):
            height_type = 'short'
        elif height in range (64, 67):
            height_type = 'medium'
        else:
            height_type = 'tall'

        topsize = int(self.request.get('topsize'))

        if topsize in range (1, 2):
            topsize_type = 'small'
        elif topsize in range (3, 5):
            topsize_type = 'medium'
        else:
            topsize_type = 'large'

        shape = 'unknown'
        image = 'unknown'

        if height_type == 'short':
            if topsize_type == 'small':
                shape = 'pear'
                image = 'pear.jpg'
            if topsize_type == 'medium':
                shape = 'carrot'
                image = 'carrot.jpg'
            if topsize_type == 'large':
                shape = 'apple'
                image = 'apple.jpg'

        if height_type == 'medium':
            if topsize_type == 'small':
                shape = 'pear'
                image = 'pear.jpg'
            if topsize_type == 'medium':
                shape = 'peanut'
                image = 'peanut.jpg'
            if topsize_type == 'large':
                shape = 'apple'
                image = 'apple.jpg'

        if height_type == 'tall':
            if topsize_type == 'small':
                shape = 'stringbean'
                image = 'stringbean.jpg'
            if topsize_type == 'medium':
                shape = 'carrot'
                image = 'carrot.jpg'
            if topsize_type == 'large':
                shape = 'stringbean'
                image = 'stringbean.jpg'

        template_vars = {'height_type':height_type,
                        'topsize_type':topsize_type,
                        'shape':shape,
                        'image':image}

        self.response.out.write(result_template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', ListHandler),
    ('/survey', SurveyHandler),
    ('/homepage', HomepageHandler),
    ('/results', ResultsHandler)
], debug=True)
