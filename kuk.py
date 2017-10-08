import random
import operator
import json

configFileName = "kukconfig.json"

people = {}
class Person(object):
	global people
	def __init__(self, name):
		self.name = name
		self.kukPoints = 0
		people[name] = self

	@classmethod
	def fromFile(self, name, kukPoints):
		person = Person(name)
		self.kukPoints = kukPoints

	@staticmethod
	def get(name):
		if name not in people:
			people[name] = Person(name)
		return people[name]

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

	@classmethod
	def fromFile(self, mid, kuk, eaters, date, flavorText):
		meal = Meal()
		meal.mid = mid
		meal.kuk = kuk
		meal.eaters = eaters
		meal.date = date
		meal.flavorText = flavorText
		mealHistory[meal.mid] = meal
		return meal

	@classmethod
	def new(self, date):
		meal = Meal()
		meal.mid = self.getNextMID()
		meal.date = date
		mealHistory[meal.mid] = meal
		return meal

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
		Meal.fromFile(meal['mid'], meal['kuk'], meal['eaters'], meal['date'], meal['flavorText'])

	try:
		with open(config['peopleFile'], 'r') as infile:
			fileData = json.load(infile)
	except:
		print "no people file!"
		return
	for person in fileData:
		Person.fromFile(person['name'], person['kukPoints'])


points = {}
points[3] = 52
points[4] = 69
points[5] = 80
points[6] = 90
points[7] = 102
points[8] = 112
points[9] = 120
points[10] = 135

newcommers = ["Rick", "Morty", "Jerry", "Mr Poopy Buthole", "Karl Gustav VII", "Erik"]

day = 1
def newDay():
	global day
	important = ['delicious', 'fabulous', 'very tasty', 'good', 'very good', 'not bad at all', 'favorable', 'ok', 'nutritious', 'italian', 'mouth-watering', 'objectively pleasing', 'aromatic', 'something to write home about', 'probably digestible', 'edible', 'a complex blend of carbon-based chemistry','not sanitized"); DROP TABLE MEALS;--', 'not poisoned', 'of unknown origin', 'crunchy', 'finger-licking good', 'fantastic', 'the best one we had so far', 'fancy', 'extrordinary', 'pleasant']
	if len(newcommers) > 0 and random.random() < 0.1:
		newbe = Person(newcommers.pop())
		newbe.attendanceRate = 0.2 + random.random() * 0.8
		print "### NEW MEMBER ###"
		print "!!! {} has joined the group !!!"
	n_people = 0
	while n_people < 3:
		attendees = []
		for name, person in people.iteritems():
			if random.random() < person.attendanceRate:
				attendees.append(name)
		
		n_people = len(attendees)
	
	print "\n\n===Day {}===".format(str(day))
	print "{} people comming: ".format(str(n_people))
	print "  ",
	for name in attendees:
		print name + ",",
	print ""

	#selecting the kuk
	cookies = [v for k,v in people.iteritems() if k in attendees]
	scookies = sorted(cookies, key=operator.attrgetter('kukPoints'), reverse=True)
	tied = []
	for person in scookies:
		if person.kukPoints < scookies[0].kukPoints:
			break
		tied.append(person)

	if len(tied)==1:
		print "{} has the most points ({}) and is going to cook".format(tied[0].name, str(tied[0].kukPoints))
		kuk = tied[0]
	else:
		print "{} people are tied with {} points each".format(str(len(tied)), str(tied[0].kukPoints))
		print "  ",
		for person in tied:
			print person.name + ",",
		print ""
		kuk = random.choice(tied)
		print "{} was selected at random and is going to cook".format(kuk.name)
	cookies.remove(kuk)

	#kuking and points 
	m = Meal.new(day);
	m.kuk = kuk.name

	reward = points[n_people]
	payment = points[n_people] / (n_people-1)
	kuk.kukPoints -= reward
	kuk.kukMealCount += 1
	kuk.kukServingCount += n_people
	kuk.eatenCount += 1
	for cookie in cookies:
		cookie.kukPoints += payment
		cookie.eatenCount += 1
		m.eaters.append(cookie.name)


	print ""
	print "{} cooked for {} people and cleared {} KukPoints".format(kuk.name, n_people, reward)
	print "{} people gained {} KukPoints each".format(n_people-1, payment)
	print "The meal was {}!".format(random.choice(important[:day]))

	day = day+1

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

		Person("Davide")
		Person("Marek")

