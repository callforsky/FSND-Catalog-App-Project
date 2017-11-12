from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# create an instance of this class. The first argument is the name of the 
# application's module or package. If you are using a single module, you should 
# use __name__ because depending on if it's started as application or imported 
# as module the name will be different ('__main__' versus the actual import 
# name)
app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Shoe Catalog"

# we now connect to the database
engine = create_engine('sqlite:///shoecatalog.db')
Base.metadata.bind = engine

# we now create the session to control the database
DBSession = sessionmaker(bind=engine)
session = DBSession()

# route decorator binds the function to a specific URL
# we want this login_page function activated only when the user is on the login 
# page
@app.route('/login')
# this function aims to create a anti-forgery state token
# this unique session token is randomized and given to the user 
# the user will have this unique state token as long as they have the same 
# login page open
def login_page():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	# Unlike a Cookie, Flask Session data is stored on server. Session is the 
	# time internal when a client logs into a server and logs out of it. The 
	# data, which is needed to be held across this session, is stored in a 
	# temporary directory on the server. For this encryption, a Flask app needs 
	# a defined secret key. In the below statement, we give the secret key that 
	# is generated earlier to user 'state'
	login_session['state'] = state
	# (note: the line below is used to test if state token is issued)
	# return "The current session state is %s" % login_session['state']
	# render_template([templateName.html, variable = keyword])
	# render_template helps the programmer to recycle the same html for 
	# more than one URL, thereby saving a lot of time.
	# the 'STATE' is a variable that we will pass to the template engine.
	# the template has to be put in the 'template' folder
	return render_template('login.html', STATE=state)

# Create the Google Connect, so the visitor can use her Google account to log on
# Make a route and function that accepts post requests
@app.route('/gconnect', methods=['POST'])
def gconnect():
	# At first, we check the state token to defend forgery attacks
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data

	# Second, need to let the program to who the developer issued the API on 
	# Goolge Oauth2. After this step, the program knows to connect to Shoe 
	# Catalog project and request the one-time access token
	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		# code is the authorization code obtained earlier, covert it to some
		# credentials
		credentials = oauth_flow.step2_exchange(code)
	# code to handle unexpected error scenarios
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid
	# Retrieve the access_token from credentials, so Google knows that it is 
	# my app requests the one-time token
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
		   % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_access_token = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_access_token is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
								 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output


# Program to revoke a current user's token and reset their login session
@app.route("/gdisconnect")
def gdisconnect():
	access_token = login_session.get('access_token')
	if access_token is None:
		print 'Access Token is None'
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.header['Content-Type'] = 'application/json'
		return response

	print 'In gdisconnect access token is %s', access_token
	print 'User name is: '
	print login_session['username']
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print 'result is '
	print result

	if result['status'] == '200':
		del login_session['access_token']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

# Create a homepage after the login page
@app.route('/')
@app.route('/shoecatalog/')
def homepage():
	categories = session.query(Category).distinct()
	items = session.query(Items)
	return render_template('homepage.html', categories=categories, items=items)

# Create a function to show the detail for a specific Category
@app.route('/shoecatalog/<int:category_id>/')
def show_one_category(category_id):
	categories = session.query(Category).distinct()
	items = session.query(Items).filter_by(category_id=category_id).all()
	return render_template('category_detail.html', categories=categories, items=items)

# Create a function to allow the user to create a new shoe category
@app.route('/shoecatalog/new/', methods=['GET','POST'])
def new_shoe_category():
	categories = session.query(Category).distinct()
	if request.method == 'POST':
		new_shoe_category = Category(name=request.form['name'])
		session.add(new_shoe_category)
		flash('New shoe category %s is created successfully!' % new_shoe_category.name)
		session.commit()
		return redirect(url_for('homepage'))
	else:
		return render_template('new_shoe_category.html', categories=categories)

# Now create a function to edit the items detail the database
@app.route('/shoecatalog/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_item(category_id):
	pass

# Create a new shoe category
# @app.route('/shoecatalog/new/', methods=['GET', 'POST'])
# def new_shoe_category():
# 	if request.method == 'POST':
# 		new_shoe_category = Category(name=request.form['category_name'])




# this part is used for
if __name__ == '__main__':
	app.secret_key = 'udacity'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)