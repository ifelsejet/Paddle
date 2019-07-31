import webapp2
from google.appengine.api import users
import logging
import jinja2
import os
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users



#Step 2: Set up Jinja environment
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
# MODELS

class Event(ndb.Model):
    activity = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
    timeDate = ndb.DateTimeProperty(required = True)
    creator = ndb.StringProperty(required = True)
    attendies = ndb.IntegerProperty(required = True, default = 1)

class Profile(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    classYear = ndb.StringProperty(required= True)

class School(ndb.Model):
    name = ndb.StringProperty(required = True)
    facility = ndb.StringProperty(required = True)

# HANDLERS

class AboutPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/about.html")
        self.response.write(template.render())

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
        #Profile.email() represents the email attributes assoiated with User models in datastore
        user = users.get_current_user()
        signin_link = users.create_login_url('/')

        email_address = user.email()
        email_match_value = Profile.query().filter(Profile.email == email_address).get()
        #creating an if statment that checks if the email used to \\
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
    # need to do queryof Event datastore
    def get(self): #for a get request
        #figure out the right filtering
        #filter for each attribu
        event_query_list = Event.query().fetch()
        print event_query_list
        #Step 3: Use the Jinja environment to get our HTML
        # for event in event_query_list :
        #
        #     event_query_list.timedate = datetime.datetime.strftime(event_query_list.timedate,"%a-%b-%d,%I %M %P"),

        template_vars = {
        'logout_link' : users.create_logout_url('/'),
        'events': event_query_list
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
    def get(self):
        template = jinja_env.get_template("templates/createEvent.html")
        self.response.write(template.render())

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

            timedate = temp_tim_obj,
            #extracting the name attribute from the right profile and
            #assigning it to the creator attribute of the model
            creator = email_match_value.name
        ).put()

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
        template = jinja_env.get_template("templates/joinEvent.html")
        self.response.write(template.render())

class Main(webapp2.RequestHandler):
        def get(self):
            template_vars = {
            'logout_link' : users.create_logout_url('/')
            }
            template = jinja_env.get_template("templates/main.html")
            self.response.write(template.render(template_vars))

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

# the app configuration section
app = webapp2.WSGIApplication([
    ('/createaccount', CreateAccount),
    ('/', SignIn_Transition), #this maps the root url to the Main Page Handler
    ('/main', Main),
    ('/joinEvent', JoinEventPage),
    ('/about', AboutPage),
    ('/createEvent', CreateNewEventPage),

], debug=True)
