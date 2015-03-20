from handler import Handler
from google.appengine.ext import db
import os
import jinja2
import datetime
import string

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Source(db.Model):
	place = db.StringProperty(required = True)

	@classmethod
	def by_place(cls, place):
		pl = Source.all().filter('place =', place).get()
		return pl
	
class Destination(db.Model):
	place = db.StringProperty(required = True)

	@classmethod
	def by_place(cls, place):
		pl = Destination.all().filter('place =', place).get()
		return pl	

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

class WelcomePage(Handler):
	def get(self):
		if self.user:
			posts = Post.all().order("-created")
			sources = db.GqlQuery("SELECT DISTINCT source FROM Post")
			self.render("Welcome_Page.html", name = self.user.name, sources = sources, posts = posts)			
		else:
			self.redirect('/?message=You seem lost, please login first')

	def post(self):
		source_searched = self.request.get('source')
		posts = Post.all().order("-created").filter("source =", source_searched)
		sources = db.GqlQuery("SELECT DISTINCT source FROM Post")
		self.render("Welcome_Page.html", name = self.user.name, sources = sources, posts = posts, message = "Search Results")			

class Post(db.Model):
	user = db.StringProperty(required = True)
	subject = db.StringProperty(required = True)
	content = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	age = db.IntegerProperty()
	source = db.StringProperty()
	destination = db.StringProperty()
	
	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		self.age = int((datetime.datetime.now() - self.created).total_seconds()/60)
		return render_str("This_Post.html", p = self)

class NewPost(Handler):
	def get(self):
		if self.user:
			sources = db.GqlQuery("SELECT DISTINCT source FROM Post")
			destinations = db.GqlQuery("SELECT DISTINCT destination FROM Post")
			self.render("New_Post.html", content = "", subject = "travelbuddy", sources = sources, destinations = destinations)
		else:
			self.redirect('/?message=You seem lost, please login first')

	def post(self):
		if not self.user:
			self.redirect('/?message=You seem lost, please login first')

		error = ""
		sources = db.GqlQuery("SELECT DISTINCT source FROM Post")
		destinations = db.GqlQuery("SELECT DISTINCT destination FROM Post")
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
				error += "Enter both source/destination or none. "		 

		if len(content) not in range(5,301) or not subject:
			error += "Include valid subject and content. Characters in your content: " + str(len(content))

		if not error:			
			p = Post(parent = blog_key(), subject = only_lowercase(subject), content = content, user = self.user.name, source = source, destination = destination)
			p.put()
			'''if source:
				s_pl = Source.by_place(source)
				d_pl = Destination.by_place(destination)
				if not s_pl:
					pl = Source(parent = place_key(), place = source)
					pl.put()
				if not d_pl:
					pl = Destination(parent = place_key(), place = destination)
					pl.put()'''
			self.redirect('/welcome')
		
		self.render("New_Post.html", subject=subject, content=content, error=error, sources = sources, destinations = destinations)

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
