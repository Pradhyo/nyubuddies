from handler import Handler 
import re

class HomePage(Handler):
	def get(self):
		self.render("Home_Page.html")

	def post(self):
		error = False
		netID = self.request.get('netID')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		params = dict(netID = netID,
					  email = email)

		if not valid_netID(netID):
			params['netID_error'] = "That's not a valid netID"
			error = True

		if not valid_password(password):
			params['password_error'] = "That's not a valid password"
			error = True
		elif verify != password:
			params['verify_error'] = "Password mismatch"
			error = True

		if not valid_email(netID, email):
			params['email_error'] = "Enter email corresponding to your NetID"
			error = True

		if error:
			self.render("Home_Page.html", **params)
		else:
			self.redirect('/welcome?name=' + netID)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{6}$")
def valid_netID(netID):
	return netID and USER_RE.match(netID)

PASS_RE = re.compile(r"^.{3,20}$")	
def valid_password(password):
	return password and PASS_RE.match(password)

def valid_email(netID, email):
	return len(email) == 14 and netID in email and '@nyu.edu' in email
