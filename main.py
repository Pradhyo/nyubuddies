import webapp2
from homepage import HomePage
from welcomepage import WelcomePage, NewPost
from signup import SignUp, EmailConfirmation, ChangePassword, DeleteAccount
from handler import LogOut, AllUsers

app = webapp2.WSGIApplication([('/', HomePage),
							   ('/signup', SignUp),
							   ('/logout', LogOut),
							   ('/delete_account', DeleteAccount),
							   #('/change_password', ChangePassword),
							   ('/email_confirmation', EmailConfirmation),
							   ('/new_post', NewPost),
							   ('/all_users', AllUsers),
							   ('/welcome', WelcomePage)], 
							   debug=True)
