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
		self.kukMealCount = 0
		self.kukServingCount = 0
		self.attendanceRate = 0.5
		self.eatenCount = 0
		people[name] = self

	@staticmethod
	def get(name):
		if name not in people:
			people[name] = Person(name)
		return people[name]

mealHistory = {}
midTop = 0

class Meal(object):
	global mealHistory
	def __init__(self, kuk, date):
		self.mid = self.getNextMID()
		self.kuk = kuk
		self.eaters = []
		self.date = date
		self.meal = "food"
		mealHistory[self.mid] = self

	@staticmethod
	def getNextMID():
		global midTop
		midTop += 1
		return midTop

def save():
	with open(config['mealHistoryFile'], 'w') as outfile:
			json.dump(mealHistory, outfile)

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
	reward = points[n_people]
	payment = points[n_people] / (n_people-1)
	kuk.kukPoints -= reward
	kuk.kukMealCount += 1
	kuk.kukServingCount += n_people
	kuk.eatenCount += 1
	for cookie in cookies:
		cookie.kukPoints += payment
		cookie.eatenCount += 1

	m = Meal(kuk.name, day);
	m.eaters = "many people"


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

	Person("Mark")
	Person("Davide")
	Person("Wille")
	Person("Sven")
	Person("David")
	Person("Ahmed")

	for name, person in people.iteritems():
		person.attendanceRate = 0.2 + random.random() * 0.8
