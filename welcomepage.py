from handler import Handler

class WelcomePage(Handler):
	def get(self):
		name = self.request.get("name")
		if self.user and self.user.name == name:
			self.render("Welcome_Page.html", name = self.user.name)
		else:
			self.redirect('/signup')