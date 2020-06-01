import atexit

from flask import Flask, render_template, request, session, redirect, url_for

from database import Database
from entity_manager import EntityManager
from util import Util
from time_unit import TimeUtil, TimeUnit
from stage import Stage

HTTP_OKAY = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403
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

def get_user():
	if 'user_id' in session:
		return entity_manager.get_user(int(session['user_id']))
	return None

@app.route('/')
def index():
	user = get_user()
	
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
			return app.response_class(status = HTTP_BAD_REQUEST)

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
	user = get_user()
	if user is not None:
		entity_manager.logout(user)

	session.pop('user_id', None)
	success_response = {
		'status': 'logout',
		'body': render_template('irms_body.html')
	}
	return Util.json_response(success_response, HTTP_OKAY)

@app.route('/listIncidents')
def list_incidents():
	user = get_user()
	incidents = entity_manager.get_incidents(user)
	data = {
		'user': user,
		'incidents': incidents,
		'incidentsLength': len(incidents)
	}
	return render_template('list_incidents.html', data = data)

@app.route('/raiseIncident', methods = ['GET', 'POST'])
def raise_incident():
	if request.method == 'POST':
		if request.is_json:
			content = request.json
		else:
			return app.response_class(status = HTTP_BAD_REQUEST)

		author = get_user()

		if author is None:
			return app.response_class(status = HTTP_FORBIDDEN)

		title = content['title']
		description = content['description']
		identificationTime = TimeUtil.sanitize_time_input(content['identificationTime'])
		implementationTime = TimeUtil.sanitize_time_input(content['implementationTime'])
		impact = entity_manager.get_impact(content['impact'])
		system = entity_manager.get_system_class(content['system'])
		priority = entity_manager.get_priority(content['priority'])
		team = entity_manager.get_team(content['team'])
		status = entity_manager.get_stage(Stage.IDENTIFYING)

		entity_manager.create_incident(title, description, author, \
			identificationTime, implementationTime, status, system, \
			impact, priority)
		return app.response_class(status = HTTP_CREATED)

	impacts = entity_manager.get_all_impacts()
	system_classes = entity_manager.get_all_system_classes()
	priorities = entity_manager.get_all_priorities()
	departments = entity_manager.get_all_departments()

	department = departments[0]
	teams = entity_manager.get_teams(department)

	data = {
		'impactsLength': len(impacts),
		'impacts': impacts,
		'prioritiesLength': len(priorities),
		'priorities': priorities,
		'systemClassesLength': len(system_classes),
		'system_classes': system_classes,
		'departmentsLength': len(departments),
		'departments': departments,
		'teamsLength': len(teams),
		'teams': teams
	}
	return render_template('raise_incident.html', data = data)

@app.route('/userNavBar')
def user_mode():
	return render_template('user_navbar.html')

@app.route('/managerNavBar')
def manager_mode():
	return render_template('manager_navbar.html')


app.run()