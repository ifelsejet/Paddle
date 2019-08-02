import webapp2
import logging
import jinja2
import os
import datetime
import json

from google.appengine.ext import ndb
from google.appengine.api import users



#Step 2: Set up Jinja environment
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
# MODELS

def joinEfxn():
    print "Hello"

class Profile(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    classYear = ndb.StringProperty(required= True)

class Event(ndb.Model):
    activity = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
    timeDate = ndb.DateTimeProperty(required = True)
    creator = ndb.StringProperty(required = True)
    attendies = ndb.KeyProperty(kind = Profile, repeated = True)

class School(ndb.Model):
    name = ndb.StringProperty(required = True)
    facility = ndb.StringProperty(required = True)

# HANDLERS

class AboutPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {
        'logout_link' : users.create_logout_url(users.create_login_url('/'))
        }
        template = jinja_env.get_template("templates/about.html")
        self.response.write(template.render(template_vars))
    def post(self):
        template_vars = {
        'logout_link' : users.create_logout_url(users.create_login_url('/'))
        }
        template = jinja_env.get_template("templates/about.html")
        self.response.write(template.render(template_vars))


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

class Main(webapp2.RequestHandler):
    def get(self):
        #filter for each attribute
        event_query_list = Event.query().order(Event.timeDate).fetch()
        #Step 3: Use the Jinja environment to get our HTML
        template_vars = {
        'logout_link' : users.create_logout_url('/'),
        'events': event_query_list
        }
        template = jinja_env.get_template("templates/main.html")
        self.response.write(template.render(template_vars))
    def post(self):

        eventkey = self.request.get('eventkey')
        event = ndb.Key(urlsafe=eventkey).get()

        #accessing current users name
        email_address = users.get_current_user().email()
        email_match_model = Profile.query().filter(Profile.email == email_address).get()
        #appening attendies
        event.attendies.append(email_match_model.key)
        event.put()
        event_query_list = Event.query().order(Event.timeDate).fetch()
        #Step 3: Use the Jinja environment to get our HTML
        template_vars = {
        'logout_link' : users.create_logout_url('/'),
        'events': event_query_list
        }
        template = jinja_env.get_template("templates/main.html")
        self.response.write(template.render(template_vars))


class CreateNewEventPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {
        'logout_link' : users.create_logout_url('/'),
        }
        template = jinja_env.get_template("templates/createEvent.html")
        self.response.write(template.render(template_vars))

    def post(self):
        activity = self.request.get("activity")
        location = self.request.get("location")
        meetingtime = self.request.get("meetingtime")
        #getting email address of logged in user
        email_address = users.get_current_user().email()
        #getting the right datastore Profile model to match with that email
        email_match_value = Profile.query().filter(Profile.email == email_address).get()
        temp_tim_obj = datetime.datetime.strptime(meetingtime,"%Y-%m-%dT%H:%M")
        Event(
            activity = activity,
            location = location,
            #parse meetingtime input string and convert top python datetime obj
            timeDate = temp_tim_obj,
            #extracting the name attribute from the right profile and
            #assigning it to the creator attribute of the model
            creator = email_match_value.name,
            attendies = [email_match_value.key]

        ).put()
        template_vars = {
        'logout_link' : users.create_logout_url('/'),
        }
        template = jinja_env.get_template("templates/main.html")
        self.response.write(template.render(template_vars))

        self.redirect("/main",True)

class JoinEventPage(webapp2.RequestHandler):
    '''
    So, whenever someone clicks the join button, we want to update the number
    of people in the event party by 1.
    Additionally, we want to also list the user's name (ex. John Doe) in the list
    of people attending.
    Finally, once the user has joined an event, we want to send an alert to show
    that they successfuly joined a certain event
    '''

    def get(self):
        # passing in event clicked variable which holds event specific id and assigninging it variable in python
        event_specific_key = self.request.get("eventclicked")
        # going through id's in datastore and matching it with the id we're looking for, then storing that event in event list
        event = ndb.Key(urlsafe=event_specific_key).get()
        template_vars = {
        "event" : event,
        'logout_link' : users.create_logout_url(users.create_login_url('/'))
        }
        template = jinja_env.get_template("templates/joinEvent.html")
        self.response.write(template.render(template_vars))


    def post(self):
        template_vars = {
        'logout_link' : users.create_logout_url(users.create_login_url('/'))
        }
        template = jinja_env.get_template("templates/joinEvent.html")
        self.response.write(template.render(template_vars))

    #def post(self):
        # event_specific_id = self.request.get("eventclicked")
        # # going through id's in datastore and matching it with the id we're looking for, then storing that event in event list
        # event_list = Event.query().filter(Event.id == event_specific_id).fetch()
        # event_list[0].attendies = event_list[0].attendies + 1


class SignIn_Transition(webapp2.RequestHandler):
    def get(self):
        """
        If email is in dataStore continue to Main Page w list of joinEvent
        creating a list that stores all the emails in dataStore.
        user.email() represents the email of the user that just logged in according to
        API docs.
        User.email() represents the email attributes
        assoicated with User models in dataStore.
        """
        user = users.get_current_user()
        signin_link = users.create_login_url('/')

        email_address = user.email()
        email_match_value = Profile.query().filter(Profile.email == email_address).get()
        #creating an if statement that checks if the email used to \\
        #login is already in datastore
        if email_match_value:
            self.redirect("/main", True)
            #created a sign out link
            #the structure of the main page
        #redirect user to make account page
        #where the create a user model with their email and extra info
        else:
            self.redirect("/createaccount", True)

class GCalendar(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/gCalendar.html")
        self.response.write(template.render())

# the app configuration section
app = webapp2.WSGIApplication([
    ('/createaccount', CreateAccount),
    ('/', SignIn_Transition), #this maps the root url to the Main Page Handler
    ('/main', Main),
    ('/joinEvent', JoinEventPage),
    ('/about', AboutPage),
    ('/createEvent', CreateNewEventPage),
    ('/calendar', GCalendar),

], debug=True)
