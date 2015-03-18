from handler import Handler
from google.appengine.ext import db
import os
import jinja2
import datetime

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment (loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class WelcomePage(Handler):
	def get(self):
		if self.user:
			posts = Post.all().order('-created')
			self.render("Welcome_Page.html", name = self.user.name, posts = posts)
		else:
			self.redirect('/?message=You seem lost, please login first')

class Post(db.Model):
    user = db.StringProperty(required = True)
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    age = db.IntegerProperty
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        self.age = int((datetime.datetime.now() - self.created).total_seconds()/60)
        return render_str("This_Post.html", p = self)

class NewPost(Handler):
    def get(self):
        if self.user:
            self.render("New_Post.html", content = "", subject = "#travelbuddy")
        else:
			self.redirect('/?message=You seem lost, please login first')

    def post(self):
        if not self.user:
			self.redirect('/?message=You seem lost, please login first')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and len(content) in range(5,301):
            p = Post(parent = blog_key(), subject = subject, content = content, user = self.user.name)
            p.put()
            self.redirect('/welcome')
        else:
            error = "Include valid subject and content. Characters in your content: " + str(len(content))
            self.render("New_Post.html", subject=subject, content=content, error=error)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)