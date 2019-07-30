#main.py
# the import section
import webapp2
from google.appengine.api import users
import logging
#Step 1: Import Jinja and os
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users

#Step 2: Set up Jinja environment
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class Profile(ndb.Model):
    name = ndb.StringProperty(required=True)
    #school = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    #phoneNumber = ndb.StringProperty(required=True)
    #Example : 2023
    classYear = ndb.StringProperty(required= True)

    def describe(self):
        return "%s goes to" % (self.name)

class School(ndb.Model):
    name = ndb.StringProperty(required = True)
    facility = ndb.StringProperty(required = True)

class CreateAccount(webapp2.RequestHandler):
    def get(self): #for a get request
        template_vars = {
        'logout_link' : users.create_logout_url(users.create_login_url('/'))
        }
        #Step 3: Use the Jinja environment to get our HTML
        template = jinja_env.get_template("templates/createAccount.html")
        self.response.write(template.render(template_vars))
    def post(self):
        #self.req.get lets us get data input
        #however we get user input from post rather than url query
        Name = self.request.get("Name")
        Email = self.request.get("Email")
        classYear = self.request.get("classYear")

        Profile(
            name = Name,
            email = users.get_current_user().email(),
            classYear = classYear,
        ).put()

        self.redirect("/main", True)

        # template = jinja_env.get_template("templates/createAccount.html")
        # self.response.write(template.render(template_vars))

class SignIn_Transition(webapp2.RequestHandler):
    def get(self):
        #if email is in datastore contue to Main Page w list of joinEvent
        #creting a list that stores all the emails in datastore
        #user.email() represents the email of the user that just logged in according to
        #api docs
        #User.email() represents the email attributes assoiated with User models in datastore

        user = users.get_current_user()
        signin_link = users.create_login_url('/')

        email_address = user.email()
        email_match_value = Profile.query().filter(Profile.email == email_address).get()
        #creating an if ststment that checks if the email used to \\
        #login is already in datastore
        if email_match_value:
            self.redirect("/main", True)
            #created a sign out link
            #the structure of the main page
        #redirect user to make account page
        #where the create a user model with their email and extra info
        else:
            self.redirect("/createaccount", True)

class Main(webapp2.RequestHandler):
    def get(self): #for a get request

        #Step 3: Use the Jinja environment to get our HTML
        template_vars = {
        'logout_link' : users.create_logout_url('/')
        }
        template = jinja_env.get_template("templates/main.html")
        self.response.write(template.render(template_vars))


class JoinEventPage(webapp2.RequestHandler):
    def get(self): #for a get request
        #Step 3: Use the Jinja environment to get our HTML
        template = jinja_env.get_template("templates/joinEvent.html")
        self.response.write(template.render())

class AboutPage(webapp2.RequestHandler):
    def get(self): #for a get request

        #Step 3: Use the Jinja environment to get our HTML
        template = jinja_env.get_template("templates/about.html")
        self.response.write(template.render())

class CreateNewEventPage(webapp2.RequestHandler):
    def get(self): #for a get request

        #Step 3: Use the Jinja environment to get our HTML
        template = jinja_env.get_template("templates/createEvent.html")
        self.response.write(template.render())
# the app configuration section
app = webapp2.WSGIApplication([
    ('/createaccount', CreateAccount),
    ('/', SignIn_Transition), #this maps the root url to the Main Page Handler
    ('/main', Main),
    ('/joinEvent', JoinEventPage),
    ('/about', AboutPage),
    ('/createEvent', CreateNewEventPage)


], debug=True)
