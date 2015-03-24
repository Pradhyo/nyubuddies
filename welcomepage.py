from handler import Handler
from google.appengine.ext import db
import os
import jinja2
import datetime
import string

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

class WelcomePage(Handler):
	def get(self):
		if self.user:
			posts = Post.all().order("-created")
			sources = db.GqlQuery("SELECT DISTINCT source FROM Post WHERE source != ''")
			self.render("Welcome_Page.html", name = self.user.name, enabled = True, sources = sources, posts = posts)			
		else:
			self.redirect('/?message=You seem lost, please login first')

	def post(self):
		source_searched = self.request.get('source')
		posts = Post.all().order("-created").filter("source =", source_searched)
		sources = db.GqlQuery("SELECT DISTINCT source FROM Post WHERE source != ''")
		self.render("Welcome_Page.html", name = self.user.name, sources = sources, posts = posts, search_message = "Search Results")			

class Post(db.Model):
	user = db.StringProperty(required = True)
	subject = db.StringProperty(required = True)
	content = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	source = db.StringProperty()
	destination = db.StringProperty()
	
	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		age = int((datetime.datetime.now() - self.created).total_seconds()/60)
		if age < 60:
			age = str(age) + 'm'
		elif age >= 1440:
			age = str(int(age/1440)) + 'd'
		elif age >=60:
			age = str(int(age/60)) + 'h'
		return render_str("This_Post.html", p = self, age = age)

class NewPost(Handler):
	def get(self):
		if self.user:
			sources = db.GqlQuery("SELECT DISTINCT source FROM Post WHERE source != ''")
			destinations = db.GqlQuery("SELECT DISTINCT destination FROM Post WHERE destination != ''")
			self.render("New_Post.html", name = self.user.name, content = "", subject = "travelbuddy", sources = sources, destinations = destinations)
		else:
			self.redirect('/?message=You seem lost, please login first')

	def post(self):
		if not self.user:
			self.redirect('/?message=You seem lost, please login first')

		error = ""
		sources = db.GqlQuery("SELECT DISTINCT source FROM Post WHERE source != ''")
		destinations = db.GqlQuery("SELECT DISTINCT destination FROM Post WHERE destination != ''")
		subject = self.request.get('subject')
		content = self.request.get('content')
		source = self.request.get('source')
		destination = self.request.get('destination')

		if source == "None":
			source = only_lowercase(self.request.get('source2'))

		if destination == "None":
			destination = only_lowercase(self.request.get('destination2'))

		if source or destination:
			if not source or not destination or source == destination:
				error += "Enter different source/destination or none. "		 

		if len(content) not in range(5,301) or not subject:
			error += "Include valid subject and content. Characters in your content: " + str(len(content))

		if not error:			
			p = Post(parent = blog_key(), subject = only_lowercase(subject), content = content, user = self.user.name, source = source, destination = destination)
			p.put()
			self.redirect('/welcome')
		
		self.render("New_Post.html", subject=subject, name = self.user.name, content=content, error=error, sources = sources, destinations = destinations)

def blog_key(name = 'default'):
	return db.Key.from_path('blogs', name)

def place_key(name = 'default'):
	return db.Key.from_path('places', name)

def only_lowercase(text):
	"""Remove digits and punctuation, then convert remaining to lowercase """
	not_allowed = string.punctuation + string.whitespace + string.digits
	text2 = [each for each in text if each not in not_allowed]
	text2 = ''.join(text2)
	return text2.lower()
