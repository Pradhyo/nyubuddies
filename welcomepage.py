from handler import Handler

class WelcomePage(Handler):
	def get(self):
		name = self.request.get("name")
		self.render("Welcome_Page.html", name = name)