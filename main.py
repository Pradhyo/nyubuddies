import webapp2
from homepage import HomePage
from welcomepage import WelcomePage, NewPost
from signup import SignUp, EmailConfirmation, ChangePassword
from handler import LogOut, DeleteAccount

app = webapp2.WSGIApplication([('/', HomePage),
							   ('/signup', SignUp),
							   ('/logout', LogOut),
							   #('/delete_account', DeleteAccount),
							   ('/change_password', ChangePassword),
							   ('/email_confirmation', EmailConfirmation),
							   ('/new_post',NewPost),
							   ('/welcome', WelcomePage)], 
							   debug=True)
