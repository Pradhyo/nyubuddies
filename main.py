import webapp2
from homepage import HomePage
from welcomepage import WelcomePage
from signup import SignUp
from handler import LogOut

app = webapp2.WSGIApplication([('/', HomePage),
							   ('/signup', SignUp),
							   ('/logout', LogOut),
							   ('/welcome', WelcomePage)], 
							   debug=True)
