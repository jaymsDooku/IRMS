import atexit

from flask import Flask, render_template, request, session, redirect, url_for

from database import Database
from entity_manager import EntityManager
from util import Util
from time_unit import TimeUtil, TimeUnit
from stage import Stage
from role import Role
from incident_value_change_request import IncidentValueChangeRequest

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
entity_manager = EntityManager(database, False)
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
		return render_template('irms.html', data = {})
	else:
		if user.role.name == Role.MAJOR_INCIDENT_MANAGER:
			incidents = entity_manager.get_all_incidents()
			pageTitle = 'All Incidents'
		else:
			incidents = entity_manager.get_incidents(user)
			pageTitle = 'Your Incidents'

		data = {
			'pageTitle': pageTitle,
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

		if user.role.name == Role.MAJOR_INCIDENT_MANAGER:
			incidents = entity_manager.get_all_incidents()
			pageTitle = 'All Incidents'
		else:
			incidents = entity_manager.get_incidents(user)
			pageTitle = 'Your Incidents'

		data = {
			'pageTitle': pageTitle,
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

	data = {}
	success_response = {
		'status': 'logout',
		'body': render_template('irms_body.html', data = data)
	}
	return Util.json_response(success_response, HTTP_OKAY)

@app.route('/decideIncidentTeam/<incident_id>/<team_id>/<decision>')
def decide_incident_team(incident_id, team_id, decision):
	incident_id = int(incident_id)
	team_id = int(team_id)

	incident = entity_manager.get_incident(incident_id)
	team = entity_manager.get_team(team_id)

	team_assignment_request = entity_manager.get_team_assignment_request(incident, team)

	if decision == 'approve':
		new_status = IncidentValueChangeRequest.STATUS_APPROVED
	elif decision == 'deny':
		new_status = IncidentValueChangeRequest.STATUS_DENIED
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	entity_manager.decide_team_assignment_request(team_assignment_request, new_status)

	return app.response_class(status = HTTP_OKAY)

@app.route('/requestIncidentTeam/<incident_id>/<team_id>')
def request_incident_team(incident_id, team_id):
	incident_id = int(incident_id)
	team_id = int(team_id)

	user = get_user()
	incident = entity_manager.get_incident(incident_id)
	team = entity_manager.get_team(team_id)

	team_assignment = entity_manager.request_team_assignment(user, incident, team)
	
	team_assignment_obj = {
		'name': team_assignment.team.name,
		'date_issued': team_assignment.date_issued,
		'assigner': (team_assignment.assigner.forename + ' ' + team_assignment.assigner.surname),
		'status': IncidentValueChangeRequest.status_to_string(team_assignment.status)
	}
	return Util.json_response(team_assignment_obj, HTTP_OKAY)

@app.route('/decideChangeRequest/<change_request_id>/<decision>')
def decide_change_request(change_request_id, decision):
	change_request_id = int(change_request_id)
	change_request = entity_manager.get_change_request(change_request_id)

	if decision == 'approve':
		new_status = IncidentValueChangeRequest.STATUS_APPROVED
	elif decision == 'deny':
		new_status = IncidentValueChangeRequest.STATUS_DENIED
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	entity_manager.decide_change_request(change_request, new_status)

	return app.response_class(status = HTTP_OKAY)

@app.route('/changeIncidentValue/<incident_id>/<value_type>', methods=['POST'])
def request_incident_value_change(incident_id, value_type):
	if request.is_json:
		content = request.json
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	incident_id = int(incident_id)
	incident = entity_manager.get_incident(incident_id)
	if incident is None:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = get_user()

	old_value = content['oldValue']
	new_value = content['newValue']
	justification = content['justification']

	change_request = entity_manager.get_existing_change_request(user, incident)

	if change_request is not None:
		entity_manager.update_change_request(change_request, new_value, justification)
	else:
		entity_manager.request_value_change(user, incident, old_value, new_value, IncidentValueChangeRequest.string_to_value_type(value_type), justification)
	return app.response_class(status = HTTP_OKAY)

@app.route('/allTeamAssignmentRequests')
def all_team_assignment_requests():
	user = get_user()
	team_assignment_requests = entity_manager.get_all_team_assignment_requests()
	data = {
		'pageTitle': 'All Requests',
		'user': user,
		'requests': team_assignment_requests,
		'requestsLength': len(team_assignment_requests),
		'requestType': 'team'
	}
	return render_template('list_requests.html', data = data)

@app.route('/listTeamAssignmentRequests')
def list_team_assignment_requests():
	user = get_user()
	#team_assignment_requests = entity_manager.get_team_assignment_requests()
	data = {
		'pageTitle': 'Your Requests',
		'user': user,
		#'requests': team_assignment_requests,
		#'requestsLength': len(team_assignment_requests),
		'requestType': 'team',
		'tab': 'team'
	}
	return render_template('list_requests.html', data = data)

@app.route('/allChangeRequests')
def all_change_requests():
	user = get_user()
	change_requests = entity_manager.get_all_change_requests()
	data = {
		'pageTitle': 'All Requests',
		'user': user,
		'requests': change_requests,
		'requestsLength': len(change_requests),
		'requestType': 'value'
	}
	return render_template('list_requests.html', data = data)

@app.route('/listChangeRequests')
def list_change_requests():
	user = get_user()
	change_requests = entity_manager.get_change_requests(user)
	data = {
		'pageTitle': 'Your Requests',
		'user': user,
		'requests': change_requests,
		'requestsLength': len(change_requests),
		'requestType': 'value'
	}
	return render_template('list_requests.html', data = data)

@app.route('/allIncidents')
def all_incidents():
	user = get_user()
	incidents = entity_manager.get_all_incidents()
	data = {
		'pageTitle': 'All Incidents',
		'user': user,
		'incidents': incidents,
		'incidentsLength': len(incidents)
	}
	return render_template('list_incidents.html', data = data)

@app.route('/listUsers') 
def list_users():
	users = entity_manager.get_users()
	data = {
		'usersLength': len(users),
		'users': users
	}
	return render_template('list_Users.html', data = data)

@app.route('/viewIncident/<incident_id>')
def view_incident(incident_id):
	incident_id = int(incident_id)
	incident = entity_manager.get_incident(incident_id)

	priorities = entity_manager.get_all_priorities()

	assigned_teams = entity_manager.get_assigned_teams(incident)
	team_assignment_requests = entity_manager.get_team_assignment_requests(incident)
	for team_assignment_request in team_assignment_requests:
		if team_assignment_request.status == IncidentValueChangeRequest.STATUS_PENDING:
			assigned_teams.append(team_assignment_request)

	departments = entity_manager.get_all_departments()

	department = departments[0]
	teams = entity_manager.get_teams(department)

	data = {
		'incident': incident,
		'priorities': priorities,
		'prioritiesLength': len(priorities),
		'assigned_teams': assigned_teams,
		'assignedTeamsLength': len(assigned_teams),
		'departmentsLength': len(departments),
		'departments': departments,
		'teamsLength': len(teams),
		'teams': teams,
		'notesLength': len(incident.notes),
		'notes': incident.notes,
		'questionsLength': len(incident.questions),
		'questions': incident.questions,
		'tasksLength': len(incident.tasks),
		'tasks': incident.tasks
	}
	return render_template('view_incident.html', data = data)

@app.route('/listIncidents')
def list_incidents():
	user = get_user()
	incidents = entity_manager.get_incidents(user)
	data = {
		'pageTitle': 'Your Incidents',
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

		sanitizedIdentificationDeadline = TimeUtil.sanitize_time_input(content['identificationDeadline'])
		sanitizedImplementationDeadline = TimeUtil.sanitize_time_input(content['implementationDeadline'])
		identificationDeadline = TimeUtil.sqlite_to_datetime(sanitizedIdentificationDeadline)
		implementationDeadline = TimeUtil.sqlite_to_datetime(sanitizedImplementationDeadline)
		impact = entity_manager.get_impact_by_level(content['impact'])
		system = entity_manager.get_system_class_by_name(content['system'])
		priority = entity_manager.get_priority_by_code(content['priority'])
		#team = entity_manager.get_team_by_name(content['team'])
		status = entity_manager.get_stage_by_level(Stage.IDENTIFYING)

		entity_manager.create_incident(title, description, author, \
			identificationDeadline, implementationDeadline, status, system, \
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

@app.route('/addNote/<incident_id>', methods=['POST'])
def add_note(incident_id):
	incident_id = int(incident_id)

	if request.is_json:
		content = request.json
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = get_user()
	incident = entity_manager.get_incident(incident_id)

	title = content['title']
	noteContent = content['content']

	entity_manager.create_note(user, incident, title, noteContent)
	return app.response_class(status = HTTP_OKAY)

@app.route('/askQuestion/<incident_id>', methods=['POST'])
def ask_question(incident_id):
	incident_id = int(incident_id)

	if request.is_json:
		content = request.json
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = get_user()
	incident = entity_manager.get_incident(incident_id)

	title = content['title']
	questionContent = content['content']

	entity_manager.create_question(user, incident, title, questionContent)
	return app.response_class(status = HTTP_OKAY)

@app.route('/addTask/<incident_id>', methods=['POST'])
def add_task(incident_id):
	incident_id = int(incident_id)

	if request.is_json:
		content = request.json
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = get_user()
	incident = entity_manager.get_incident(incident_id)

	title = content['title']
	taskContent = content['content']

	entity_manager.create_task(user, incident, title, taskContent)
	return app.response_class(status = HTTP_OKAY)

@app.route('/departmentTeams/<department_name>')
def get_teams(department_name):
	department = entity_manager.get_department_by_name(department_name)
	teams = entity_manager.get_teams(department)
	team_objects = []
	for team in teams:
		team_objects.append({ 'team_id': team.id, 'team_name': team.name})
	return Util.json_response({ 'teams': team_objects }, HTTP_OKAY)

@app.route('/userNavBar')
def user_mode():
	return render_template('user_navbar.html')

@app.route('/managerNavBar')
def manager_mode():
	return render_template('manager_navbar.html')


app.run()