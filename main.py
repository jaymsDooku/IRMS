import atexit

from flask import Flask, render_template, request, session, redirect, url_for

from database import Database
from entity_manager import EntityManager
from util import Util

HTTP_OKAY = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_UNPROCESSABLE = 422
HTTP_SERVER_ERROR = 500

app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

database = Database('irms.db')
entity_manager = EntityManager(database, True)
entity_manager.initialize()

def handle_shutdown():
	database.close()

atexit.register(handle_shutdown)

@app.route('/')
def index():
	user = None
	if 'user_id' in session:
		user = entity_manager.get_user(int(session['user_id']))
	
	if user is None:
		return render_template('irms.html')
	else:
		incidents = entity_manager.get_all_incidents()
		data = {
			'user': user,
			'incidents': incidents,
			'incidentsLength': len(incidents)
		}
		return render_template('irms.html', data = data)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.is_json:
			content = request.json
		else:
			return app.response_class(status = self.HTTP_BAD_REQUEST)

		username = content['username']
		password = content['password']

		user = entity_manager.get_user_by_username(username)

		if user is None:
			return Util.json_response({'status': 'invalid credential'}, HTTP_OKAY)

		if user.password != password:
			return Util.json_response({'status': 'invalid credential'}, HTTP_OKAY)

		entity_manager.login(user)
		session['user_id'] = str(user.id)

		incidents = entity_manager.get_all_incidents()
		data = {
			'user': user,
			'incidents': incidents,
			'incidentsLength': len(incidents)
		}
		success_response = {
			'status': 'success',
			'body': render_template('irms_body.html', data = data)
		}
		response = Util.json_response(success_response, HTTP_OKAY)
		return response

@app.route('/logout')
def logout():
	user_id = session['user_id']
	user = entity_manager.get_user(user_id)
	entity_manager.logout(user)

	session.pop('user_id', None)
	success_response = {
		'status': 'logout',
		'body': render_template('irms_body.html')
	}
	return Util.json_response(success_response, HTTP_OKAY)

@app.route('/raiseIncident')
def raise_incident():
	return render_template('raise_incident.html')

@app.route('/userNavBar')
def user_mode():
	return render_template('user_navbar.html')

@app.route('/managerNavBar')
def manager_mode():
	return render_template('manager_navbar.html')


app.run()