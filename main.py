from os import path
import atexit
import csv

from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory

from database import Database
from entity_manager import EntityManager
from util import Util
from time_unit import TimeUtil, TimeUnit
from stage import Stage
from role import Role
from incident_value_change_request import IncidentValueChangeRequest
from datetime import timedelta

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

def add_dates(data, incidents):
	if len(incidents) > 0:
		startDate = incidents[0].date_created
		endDate = incidents[0].date_created
		for incident in incidents:
			if incident.date_created < startDate:
				startDate = incident.date_created
			if incident.date_created > endDate:
				endDate = incident.date_created

		if startDate == endDate:
			endDate = endDate + timedelta(minutes=1)
		data['startDate'] = TimeUtil.datetime_to_string(startDate)
		data['endDate'] = TimeUtil.datetime_to_string(endDate)

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

		notifications = entity_manager.get_user_notifications(user)

		data = {
			'pageTitle': pageTitle,
			'user': user,
			'incidents': incidents,
			'incidentsLength': len(incidents),
			'notifications': notifications,
			'notificationsLength': len(notifications)
		}

		add_dates(data, incidents)

		print(data)
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

		notifications = entity_manager.get_notifications(user)

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

	user = get_user()
	entity_manager.decide_team_assignment_request(user, team_assignment_request, new_status)

	return app.response_class(status = HTTP_OKAY)

@app.route('/decideTaskTeam/<task_id>/<team_id>/<decision>')
def decide_task_team(task_id, team_id, decision):
	task_id = int(task_id)
	team_id = int(team_id)

	task = entity_manager.get_task(task_id)
	team = entity_manager.get_team(team_id)

	team_assignment_request = entity_manager.get_team_assignment_request(task, team)

	if decision == 'approve':
		new_status = IncidentValueChangeRequest.STATUS_APPROVED
	elif decision == 'deny':
		new_status = IncidentValueChangeRequest.STATUS_DENIED
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = get_user()
	entity_manager.decide_team_assignment_request(user, team_assignment_request, new_status)

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

@app.route('/requestTaskTeam/<task_id>/<team_id>')
def request_task_team(task_id, team_id):
	task_id = int(task_id)
	team_id = int(team_id)

	user = get_user()
	task = entity_manager.get_task(task_id)
	team = entity_manager.get_team(team_id)

	team_assignment = entity_manager.request_team_assignment(user, task, team)
	
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

	user = get_user()
	entity_manager.decide_change_request(user, change_request, new_status)

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

	value_type = IncidentValueChangeRequest.string_to_value_type(value_type)
	change_request = entity_manager.get_existing_change_request(user, incident, value_type)

	if change_request is not None:
		entity_manager.update_change_request(user, change_request, new_value, justification)
	else:
		entity_manager.request_value_change(user, incident, old_value, new_value, value_type, justification)
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

	add_dates(data, incidents)

	return render_template('list_incidents.html', data = data)

@app.route('/listUsers') 
def list_users():
	roles = entity_manager.get_all_roles()
	users = entity_manager.get_users()
	data = {
		'usersLength': len(users),
		'users': users,
		'rolesLength': len(roles),
		'roles': roles
	}
	return render_template('list_Users.html', data = data)

@app.route('/updateRole/<user_id>', methods=['POST'])
def update_user_role(user_id):
	user_id = int(user_id)

	if request.is_json:
		content = request.json
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = entity_manager.get_user(user_id)
	role_name = content['role']
	new_role = entity_manager.get_role_by_name(role_name)

	entity_manager.update_user_role(user, new_role)

	return app.response_class(status = HTTP_OKAY)

@app.route('/viewIncident/<incident_id>')
def view_incident(incident_id):
	incident_id = int(incident_id)
	incident = entity_manager.get_incident(incident_id)

	impacts = entity_manager.get_all_impacts()
	priorities = entity_manager.get_all_priorities()
	severities = entity_manager.get_all_severities()

	assigned_teams = entity_manager.get_assigned_teams(incident)
	team_assignment_requests = entity_manager.get_team_assignment_requests(incident)
	for team_assignment_request in team_assignment_requests:
		if team_assignment_request.status == IncidentValueChangeRequest.STATUS_PENDING:
			assigned_teams.append(team_assignment_request)

	departments = entity_manager.get_all_departments()

	department = departments[0]
	teams = entity_manager.get_teams(department)

	user = get_user()

	for task in incident.tasks:
		print(task.teams)

	data = {
		'user': user,
		'incident': incident,
		'priorities': priorities,
		'prioritiesLength': len(priorities),
		'impacts': impacts,
		'impactsLength': len(impacts),
		'severities': severities,
		'severitiesLength': len(severities),
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
		'incidentsLength': len(incidents),
	}

	add_dates(data, incidents)

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
		severity = entity_manager.get_severity_by_code(content['severity'])
		system = entity_manager.get_system_class_by_name(content['system'])
		priority = entity_manager.get_priority_by_code(content['priority'])
		#team = entity_manager.get_team_by_name(content['team'])
		status = entity_manager.get_stage_by_level(Stage.IDENTIFYING)

		entity_manager.create_incident(title, description, author, \
			identificationDeadline, implementationDeadline, status, system, \
			impact, priority, severity)
		return app.response_class(status = HTTP_CREATED)

	severities = entity_manager.get_all_severities()
	impacts = entity_manager.get_all_impacts()
	system_classes = entity_manager.get_all_system_classes()
	priorities = entity_manager.get_all_priorities()
	departments = entity_manager.get_all_departments()

	department = departments[0]
	teams = entity_manager.get_teams(department)

	user = get_user()

	data = {
		'user': user,
		'impactsLength': len(impacts),
		'impacts': impacts,
		'prioritiesLength': len(priorities),
		'priorities': priorities,
		'severitiesLength': len(severities),
		'severities': severities,
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

@app.route('/viewNote/<note_id>')
def view_note(note_id):
	note_id = int(note_id)

	note = entity_manager.get_note(note_id)

	data = {
		'note': note
	}
	return render_template('view_note.html', data = data)

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

@app.route('/answerQuestion/<question_id>', methods=['POST'])
def answer_question(question_id):
	question_id = int(question_id)

	if request.is_json:
		content = request.json
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = get_user()
	question = entity_manager.get_question(question_id)

	answer = content['answer']

	entity_manager.answer_question(user, question, answer)
	return app.response_class(status = HTTP_OKAY)

@app.route('/viewQuestion/<question_id>')
def view_question(question_id):
	question_id = int(question_id)

	question = entity_manager.get_question(question_id)

	data = {
		'question': question
	}
	return render_template('view_question.html', data = data)

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

@app.route('/followIncident/<incident_id>')
def follow_incident(incident_id):
	incident_id = int(incident_id)

	user = get_user()
	incident = entity_manager.get_incident(incident_id)

	entity_manager.follow(user, incident)

	return app.response_class(status = HTTP_OKAY)

@app.route('/notifications')
def notifications():
	user = get_user()
	if user is None:
		return app.response_class(status = HTTP_OKAY)

	notifications = entity_manager.get_user_notifications(user)

	unseen = 0
	for notification in notifications:
		if not notification.seen:
			unseen += 1
			entity_manager.seen_user_notification(notification)

	data = {
		'notifications': notifications,
		'notificationsLength': len(notifications)
	}

	json_response = {
		'unseen': unseen,
		'body': render_template('notification-body.html', data = data)
	}
	return Util.json_response(json_response, HTTP_OKAY)

@app.route('/allUsers')
def usernames():
	users = entity_manager.get_users()
	users_response = []
	for user in users:
		name = user.forename + ' ' + user.surname
		users_response.append({ 'id': user.id, 'name': name})

	return Util.json_response({ 'users': users_response }, HTTP_OKAY)

@app.route('/exportCSV/<incident_id>')
def export_csv(incident_id):
	incident_id = int(incident_id)
	incident = entity_manager.get_incident(incident_id)

	reportsDir = path.join(app.root_path, 'reports')
	filename = 'incident' + str(incident_id) + '.csv'

	with open(reportsDir + '/' + filename, mode='w', newline='', encoding='utf-8') as csv_file:
		writer = csv.writer(csv_file, delimiter=",")
		incident.to_csv(writer)

	return send_from_directory(directory = reportsDir, filename = filename)

@app.route('/listExportCSV', methods=['POST'])
def list_export_csv():
	if request.is_json:
		content = request.json
	else:
		return app.response_class(status = HTTP_BAD_REQUEST)

	user = get_user()
	start = content['startDate']
	end = content['endDate']
	incidentIds = content['incidents']
	incidents = []
	for incidentId in incidentIds:
		incidents.append(entity_manager.get_incident(int(incidentId)))

	startDate = TimeUtil.sqlite_to_datetime(TimeUtil.sanitize_time_input(start))
	endDate = TimeUtil.sqlite_to_datetime(TimeUtil.sanitize_time_input(end))
	selectedIncidents = []

	for incident in incidents:
		print(type(incident.date_created))
		print(type(startDate))
		print(type(endDate))
		if incident.date_created >= startDate and incident.date_created <= endDate:
			selectedIncidents.append(incident)

	current_date = TimeUtil.now()
	reportsDir = path.join(app.root_path, 'reports')
	filename = 'incident' + current_date.strftime('%Y_%m_%d_%H_%M_%S') + '.csv'

	with open(reportsDir + '/' + filename, mode='w', newline='', encoding='utf-8') as csv_file:
		writer = csv.writer(csv_file, delimiter=",")
		writer.writerow(["ID", "Title", "Description", "Author", "SLA Identification Deadline", "Date Identified", \
	        	"SLA Implementation Deadline", "Date Implemented", "Status", "System", "Impact", "Priority", "Severity", "Note Count", \
	        	"Question Count", "Task Count"])
		for incident in selectedIncidents:
			author_name = incident.author.forename + ' ' + incident.author.surname
			writer.writerow([incident.id, incident.title, incident.description, author_name, incident.sla_identification_deadline, incident.date_identified, incident.sla_implementation_deadline, incident.date_implemented, \
				incident.status.level, incident.system.name, incident.impact.level, incident.priority.code, incident.severity.code, len(incident.notes), len(incident.questions), len(incident.tasks)])

	return send_from_directory(directory = reportsDir, filename = filename)


@app.route('/resolutionIdentified/<incident_id>')
def identified(incident_id):
	incident_id = int(incident_id)
	incident = entity_manager.get_incident(incident_id)

	user = get_user()
	entity_manager.update_incident_identified_date(user, incident)
	status = incident.status
	date = incident.date_identified

	return Util.json_response({ 'status': status.level, 'status_class': status.get_class(), 'date': date }, HTTP_OKAY)

@app.route('/resolutionImplemented/<incident_id>')
def implemented(incident_id):
	incident_id = int(incident_id)
	incident = entity_manager.get_incident(incident_id)

	user = get_user()
	entity_manager.update_incident_implemented_date(user, incident)
	status = incident.status
	date = incident.date_implemented

	return Util.json_response({ 'status': status.level, 'status_class': status.get_class(), 'date': date }, HTTP_OKAY)

@app.route('/userNavBar')
def user_mode():
	user = get_user()
	data = {
		'user': user
	}
	return render_template('user_navbar.html', data = data)

@app.route('/managerNavBar')
def manager_mode():
	user = get_user()
	data = {
		'user': user
	}
	return render_template('manager_navbar.html', data = data)


app.run()