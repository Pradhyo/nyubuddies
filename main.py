import webapp2
from homepage import HomePage
from welcomepage import WelcomePage
from signup import SignUp, EmailConfirmation
from handler import LogOut

app = webapp2.WSGIApplication([('/', HomePage),
							   ('/signup', SignUp),
							   ('/logout', LogOut),
							   ('/email_confirmation', EmailConfirmation),
							   ('/welcome', WelcomePage)], 
							   debug=True)
