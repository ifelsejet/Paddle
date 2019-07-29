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

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    #school = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    #phoneNumber = ndb.StringProperty(required=True)
    #Example : 2023
    classYear = ndb.IntegerProperty(required= True)

    def describe(self):
        return "%s goes to" % (self.name)

class School(ndb.Model):
    name = ndb.StringProperty(required = True)
    facility = ndb.StringProperty(required = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        #if email is in datastore contue to Main Page w list of joinEvent
        #creting a list that stores all the emails in datastore
        user_list = User.query().fetch().email()

        #creating an if ststment that checks if the email used to \
        #login is already in datastore
        # if (login.email() in user_list):
        #     #the structure of the main page
        #
        # #redirect user to make account page
        # #where the create a user model with their email and extra info
        # else ()


        #for a get request
        #Step 3: Use the Jinja environment to get our HTML
        template = jinja_env.get_template("templates/main.html")
        self.response.write(template.render())

class CreateAccount(webapp2.RequestHandler):
    def get(self): #for a get request

        #Step 3: Use the Jinja environment to get our HTML
        template = jinja_env.get_template("templates/joinEvent.html")
        self.response.write(template.render())

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
    ('/', MainPage), #this maps the root url to the Main Page Handler
    ('/joinEvent' , JoinEventPage),
    ('/about', AboutPage),
    ('/createEvent', CreateNewEventPage)


], debug=True)
