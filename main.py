#main.py
# the import section
import webapp2
from google.appengine.api import users
import logging
#Step 1: Import Jinja and os
import jinja2
#import urllib
#import json
import os

from google.appengine.ext import ndb
from google.appengine.api import users
#from google.appengine.api import urlfetch


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
        #Python API Notes
        '''
        Set up my key (in GCP console) and url
        api_key = 'something1234567'
        params = {'q': 'Harry Potter',
        'api_key': api_key}
        base_url = 'url'
        full_url = base_url + '?' + urllib.urlencode(params)

        Fetch the url (service name [in GCP])
        response  = urlfetch.fetch(full_url).content


        Get the JSON response and convert to dictionary
        response_dictonary = json.loads(response)

        template_vars = {
        'books': books_dictionary['items'],
        }
        '''
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
class FlexBoxPage(webapp2.RequestHandler):
    def get(self): #for a get request

        #Step 3: Use the Jinja environment to get our HTML
        template = jinja_env.get_template("templates/flexboxTest.html")
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
    ('/createEvent', CreateNewEventPage),
    ('/flex', FlexBoxPage)


], debug=True)
