import random
import operator
import json
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
app = Flask(__name__)

#config
app.config.update(
   DEBUG = True,
   SECRET_KEY = 'secret_xxx'
)
configFileName = "kukconfig.json"
try:
	with open (configFileName, 'r') as configFile:
		config = json.load(configFile)
except IOError:
	print "Config file not found! Loading defaults"
	config = {}
	config['ip'] = '127.0.0.1'
	config['port'] = 5000
	config['debug'] = True
	config['mealHistoryFile'] = "MealHistory.json"
	config['peopleFile'] = "People.json"

people = {}
class Person(UserMixin):
	global people
	def __init__(self, name):
		self.name = name
		self.id = name
		self.kukPoints = 0
		self.password = ''
		people[name] = self

	@classmethod
	def fromFile(self, name, kukPoints, password):
		person = Person(name)
		person.kukPoints = kukPoints
		person.password = password

	@staticmethod
	def get(name):
		if name not in people:
			people[name] = Person(name)
		return people[name]

	@staticmethod
	def leaderboard():
		leaderboard = []
		for name,person in people.iteritems():
			entry = {}
			entry['name'] = name
			entry['score'] = person.kukPoints
			leaderboard.append(entry)
		leaderboard.sort(key=lambda tup : tup['score'], reverse = True)
		return leaderboard

	def serialized(self):
		return self.__dict__

mealHistory = {}

class Meal(object):
	global mealHistory
	def __init__(self):
		self.mid = ''
		self.kuk = ''
		self.eaters = []
		self.date = ''
		self.flavorText = ''
		self.accounted = ""

	@classmethod
	def fromFile(self, mid, kuk, eaters, date, flavorText, accounted):
		meal = Meal()
		meal.mid = mid
		meal.kuk = kuk
		meal.eaters = eaters
		meal.date = date
		meal.flavorText = flavorText
		meal.accounted = accounted
		mealHistory[meal.mid] = meal
		return meal

	@classmethod
	def new(self, date):
		meal = Meal()
		meal.mid = self.getNextMID()
		meal.date = date
		meal.accounted = "no"
		mealHistory[meal.mid] = meal
		return meal

	def account(self):
		if self.accounted != "no":
			return "ERROR! this meal has already been accounted for or is broken!"
		self.accounted = "yes"
		eaterCount = len(self.eaters)
		points = config['points'][eaterCount]
		print "kuk {} clears {} points".format(self.kuk, points)
		Person.get(self.kuk).kukPoints -= points
		for eater in self.eaters:
			Person.get(eater).kukPoints += points / eaterCount
			print "+{} gets {} points ".format(eater, points / eaterCount)

	@staticmethod
	def getNextMID():
		if len(mealHistory) == 0:
			return 1
		return max(mealHistory.keys())+1

	def serialized(self):
		return self.__dict__

def save():
	with open(config['mealHistoryFile'], 'w') as outfile:
		mealListJson = []
		for mid,meal in mealHistory.iteritems():
			mealListJson.append(meal.serialized())
		json.dump(mealListJson, outfile)

	with open(config['peopleFile'], 'w') as outfile:
		peopleJson = []
		for name,person in people.iteritems():
			peopleJson.append(person.serialized())
		json.dump(peopleJson, outfile)

def load():
	mealHistory = {}
	people = {}
	try:
		with open(config['mealHistoryFile'], 'r') as infile:
			fileData = json.load(infile)
	except:
		print "no meal history file!"
		return
	for meal in fileData:
		Meal.fromFile(meal['mid'], meal['kuk'], meal['eaters'], meal['date'], meal['flavorText'], meal['accounted'])

	try:
		with open(config['peopleFile'], 'r') as infile:
			fileData = json.load(infile)
	except:
		print "no people file!"
		return
	for person in fileData:
		Person.fromFile(person['name'], person['kukPoints'], person['password'])
load()

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route("/")
@login_required
def index():
	cook = {}
	cook['name'] = 'Ahmed'
	cook['confirmed'] = 'no'

	eaters = ['Marek', 'Davide', 'Sven']
	return render_template('index.html', leaderboard=Person.leaderboard(), cook=cook, eaters=eaters)

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print len(people)
        if Person.get(username).password == password:
	        login_user(Person.get(username))
	        return redirect(request.args.get("next"))
        return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return Person.get(userid)

if __name__ == '__main__':
	try:
		with open (configFileName, 'r') as configFile:
			config = json.load(configFile)
	except IOError:
		print "Config file not found! Loading defaults"
		config = {}
		config['ip'] = '127.0.0.1'
		config['port'] = 5000
		config['debug'] = True
		config['mealHistoryFile'] = "MealHistory.json"
		config['peopleFile'] = "People.json"
	load()