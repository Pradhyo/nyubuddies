from handler import Handler, User, make_pw_hash
import re
from google.appengine.api import mail

class SignUp(Handler):
	def get(self):
		self.render("Signup.html", message = "Signup here", not_logged = True)

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
			params['not_logged'] = True
			self.render("Signup.html", **params)
		else:
			self.done()

	def done(self):
		#make sure the user doesn't already exist
		u = User.by_name(self.netID)
		if u:
			msg = 'That user already exists.'
			self.render('Signup.html', netID_error = "User already exists", not_logged = True)
		else:
			sender_address = "NYU Buddies <bpradhyo@gmail.com>"
			user_address = self.email
			subject = "Confirm your registration"
			self.pw_hash = make_pw_hash(self.netID,self.password)
			u = User.register(self.netID, self.pw_hash, self.email, False)
			u.put()
			confirmation_url = "?netID=%s&pw_hash=%s&email=%s" %(self.netID, self.pw_hash, self.email)
			body = """ The url is nyubuddies.appspot.com/email_confirmation%s """ %confirmation_url
			mail.send_mail(sender_address, user_address, subject, body)
			self.write("Check your email")


USER_RE = re.compile(r"^[a-z0-9]{6}$")
def valid_netID(netID):
	return netID and USER_RE.match(netID) and netID[3:].isdigit()

PASS_RE = re.compile(r"^.{3,20}$")	
def valid_password(password):
	return password and PASS_RE.match(password)

def valid_email(netID, email):
	return len(email) == 14 and netID in email and '@nyu.edu' in email

class EmailConfirmation(Handler):
	def get(self):
		self.netID = self.request.get("netID")
		self.pw_hash = self.request.get("pw_hash")
		self.email = self.request.get("email")
		u = User.by_name(self.netID)
		if u and not u.confirm_email and len(self.pw_hash) == 70:
			u = User.register(self.netID, self.pw_hash, self.email, True)
			u.put()
			self.redirect('/?message=Your email has been successfully verified')
		else:
			self.redirect('/?message=You seem lost, please login first')

class ChangePassword(SignUp):
	def get(self):
		u = self.user
		if u:
			self.render("Signup.html", message = "Change your password here")			
		else:
			self.redirect('/?message=You seem lost, please login first')

	def done(self):
		u = self.user
		if u:
			self.pw_hash = make_pw_hash(self.netID,self.password)
			u.delete()
			u = User.register(self.netID, self.pw_hash, self.email, True)
			u.put()
			self.redirect('/?message=You have successfully changed your password')			
		else:
			self.redirect('/?message=You seem lost, please login first')

			