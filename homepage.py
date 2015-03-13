from handler import Handler 
import re

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
		elif verify != password:
			params['verify_error'] = "Password mismatch"
			error = True

		if not valid_email(email):
			params['email_error'] = "Not a valid email"
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
