from flask import Flask, render_template, request, flash, redirect, url_for, session, make_response
from wtforms import Form, StringField, validators	
import urllib2
from readData import *
from pprint import pprint

app = Flask(__name__)

class LoginForm(Form):
	name = StringField( 'Name ', [ validators.Length(min=4, max=25) , validators.DataRequired() ])

@app.route('/', methods=[ 'GET','POST' ])
def submit():

	form 	 = LoginForm(request.form)

	color 	 = getColor()

	if request.method == 'POST' and form.validate():

		name = request.form['name']

		flash('Thanks for logging in')
		counter()

		resp = app.make_response(redirect(url_for('home', username=name)))
		resp.set_cookie('usernameCookie', name )
		
		return resp

	else:

		cookie = getCookieUsername()

		return render_template('login.html', form=form, cookieName= cookie, color=color)


@app.route('/home/<username>', methods=[ 'GET', 'POST' ])
def home(username):

	username 	= getCookieUsername()
	color 		= getColor()
	
	namesWinners = query_db('SELECT id, year, surname from nobelPrize')

	if request.method == 'POST':

		if request.form['submit'] == "Change color":

			session['color'] = request.form['colors']
			color = getColor()

		elif request.form['submit'] == "Request Nobelprize data":

			get_db()
			readJson()

			namesWinners = query_db('SELECT id, year, surname from nobelPrize')

			print 'Data imported into database.'

		return render_template('home.html', color= color, name= username, numberOfLogins= session[ 'counter'], namesWinners= namesWinners)
	else:

		return render_template('home.html', name= username, color= color, numberOfLogins= session[ 'counter' ], namesWinners= namesWinners)

@app.route('/prizewinner/<id>')
def prizewinner(id):

	prizeWinner = query_db('SELECT * FROM nobelPrize WHERE id = ?', [id])

	name    = getCookieUsername()
	color 	= getColor()

 	return render_template('nobelprizes.html', color= color, prizeWinner=prizeWinner, name= name)

@app.route('/deletePrizewinner/<id>')
def deletePrizewinner(id):

	get_db().execute('DELETE FROM nobelPrize WHERE id= ?', [id])
	get_db().commit()

	flash('Prizewinner deleted from database!')

	name = getCookieUsername()

	return redirect(url_for('home', username= name))

@app.route('/updatePrizewinner/<id>', methods=[ 'GET', 'POST' ])
def updatePrizewinner(id):

	prizeWinner = query_db('SELECT * FROM nobelPrize WHERE id= ?', [id])

	name 	= getCookieUsername()
	color 	= getColor()

	if request.method == 'POST':

		category 			= request.form['category']
		year 			 	= request.form['year']
		overallMotivation 	= request.form['overallMotivation']
		firstname 			= request.form['firstname']
		surname				= request.form['surname']
		share				= request.form['share']
		motivation 			= request.form['motivation']

		get_db().execute("UPDATE nobelPrize SET year= ?, category= ?, overallMotivation= ?, firstname= ?, surname= ?, share= ?, motivation=? WHERE id= ?", [year,category, overallMotivation, firstname, surname, share, motivation, id])
		get_db().commit()

		flash('Data updated!')

		return redirect(url_for('home', username= name))
	else:
 		return render_template('update.html', color= color, prizeWinner=prizeWinner, name= name)


def counter():
	
	if 'counter' in session.keys():
		session['counter'] += 1
	else:
		session['counter'] = 1


def getColor():

	if 'color' in session.keys():
		color = session['color']
	else:
		color = 'white'

	return color

def getCookieUsername():

    if(request.cookies.get('usernameCookie')):
        mycookie = request.cookies.get('usernameCookie')
        return mycookie    

if __name__ == "__main__":
	app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
	app.run(debug=True)
