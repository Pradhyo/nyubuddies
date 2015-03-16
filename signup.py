from handler import Handler, User
import re
#import string

class SignUp(Handler):
	def get(self):
		self.render("Signup.html")

	def post(self):
		error = False
		self.netID = self.request.get('netID')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')
		self.email = self.request.get('email')

		params = dict(netID = self.netID,
					  email = self.email)

		if not valid_netID(self.netID):
			params['netID_error'] = "That's not a valid netID"
			error = True

		if not valid_password(self.password):
			params['password_error'] = "That's not a valid password"
			error = True
		elif self.verify != self.password:
			params['verify_error'] = "Password mismatch"
			error = True

		if not valid_email(self.netID, self.email):
			params['email_error'] = "Enter email corresponding to your NetID"
			error = True

		if error:
			self.render("Signup.html", **params)
		else:
			self.done()

	def done(self):
		#make sure the user doesn't already exist
		u = User.by_name(self.netID)
		if u:
			msg = 'That user already exists.'
			self.render('Signup.html', netID_error = "User already exists")
		else:
			u = User.register(self.netID, self.password, self.email)
			u.put()

			self.login(u)
			self.redirect('/welcome?name=' + netID)

USER_RE = re.compile(r"^[a-z0-9]{6}$")
def valid_netID(netID):
	return netID and USER_RE.match(netID) and netID[3:].isdigit()

PASS_RE = re.compile(r"^.{3,20}$")	
def valid_password(password):
	return password and PASS_RE.match(password)

def valid_email(netID, email):
	return len(email) == 14 and netID in email and '@nyu.edu' in email
