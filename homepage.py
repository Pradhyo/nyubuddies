from handler import Handler, User

class HomePage(Handler):
    def get(self):
        self.render('Home_Page.html', message = self.request.get('message'), not_logged = True)

    def post(self):
        netID = self.request.get('netID')
        password = self.request.get('password')

        u = User.login(netID, password)
        if u:
            self.login(u)
            self.redirect('/welcome?name=' + netID)
        else:
            msg = 'Invalid login'
            self.render('Home_Page.html', error = msg, not_logged = True)