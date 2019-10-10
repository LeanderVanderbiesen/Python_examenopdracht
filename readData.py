from flask import Flask,g
import json
import sqlite3
import urllib2

DATABASE= 'database/vanderbiesen_leander.db'


def readJson():

	urlData = "http://api.nobelprize.org/v1/prize.json"

	try:

		con = urllib2.urlopen(urlData)

		print 'Connected to database.'

		years 				=[]
		category 			=[]
		overallMotivation 	=[]
		laureates 			=[]

		personId 			=[]
		firstname 			=[]
		surname 			=[]
		motivation 			=[]
		share 				=[]

		if con.getcode() == 200:

			data = con.read()
			output = json.loads(data)

			for line in output["prizes"]:
				years.append( line["year"])
				category.append(line["category"])
				laureates.append(line["laureates"])

				if 'overallMotivation' in line.keys():
					overallMotivation.append(line["overallMotivation"])
				else:
					overallMotivation.append("No overall motivation")

				for priceWinners in line["laureates"]:
					personId.append(priceWinners["id"])
					firstname.append(priceWinners["firstname"])
					surname.append(priceWinners["surname"])

					if 'motivation' in priceWinners.keys():
						motivation.append(priceWinners["motivation"])
					else:
						motivation.append("No motivation")

					share.append(priceWinners["share"])

			for x in xrange(0,20):
				get_db().execute("INSERT INTO nobelPrize (id, year, category, firstname, surname,  share, motivation, overallMotivation)\
				VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (personId[x], years[x], category[x], firstname[x], surname[x], share[x], motivation[x], overallMotivation[x]))
				
				get_db().commit()

	except urllib2.HTTPError, e:
		return e.getcode()

def get_db():
	db = getattr(g, '_database', None)
	try:
		if db is None:
			db = g._database = sqlite3.connect(DATABASE)
			db.execute("CREATE TABLE IF NOT EXISTS nobelPrize (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, year INTEGER NOT NULL, category TEXT NOT NULL, firstname TEXT NOT NULL, surname TEXT NOT NULL, share INTEGER NOT NULL, motivation TEXT, overallMotivation TEXT);")	
		return db
	except Error as e:
		print e

def query_db(query, args=()):
	try:
		cur = get_db().execute(query, args)
		rv = cur.fetchall()
		cur.close()
		return rv
	except sqlite3.Error as e:
		print e
	
	