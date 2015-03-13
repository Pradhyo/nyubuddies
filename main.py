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
import webapp2
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self,template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class HomePage(Handler):
	def get(self):
		self.render("Home_Page.html")

	def post(self):
		error = False
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		params = dict(username = username,
					  email = email)

		if not valid_username(username):
			params['username_error'] = "That's not a valid username"
			error = True

		if not valid_password(password):
			params['password_error'] = "That's not a valid password"
			error = True

		if verify != password:
			params['verify_error'] = "Password mismatch"
			error = True

		if error:
			self.render("Home_Page.html", **params)
		else:
			self.redirect('/welcome?name=' + username)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")	
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')	
def valid_email(email):
	return not email or EMAIL_RE.match(email)

class WelcomePage(Handler):
	def get(self):
		name = self.request.get("name")
		self.render("Welcome_Page.html", name = name)

app = webapp2.WSGIApplication([('/', HomePage),
								('/welcome', WelcomePage)], 
								debug=True)
