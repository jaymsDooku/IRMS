from role import Role
from user import User
from department import Department
from team import Team
from impact import Impact
from priority import Priority
from severity import Severity
from stage import Stage
from system_class import SystemClass
from incident import Incident
from user_session import UserSession
from incident_value_change_request import IncidentValueChangeRequest
from team_assignment_request import TeamAssignmentRequest
from assigned_team import AssignedTeam
from note import Note
from question import Question
from answer import Answer
from task import Task
from follow import Follow
from notification import Notification
from user_notification import UserNotification

from time_unit import TimeUtil, TimeUnit

class EntityManager:

	def __init__(self, database, clearOnStartUp):
		self.impacts = {}
		self.priorities = {}
		self.severities = {}
		self.stages = {}
		self.system_classes = {}

		self.roles = {}
		self.users = {}
		self.departments = {}
		self.teams = {}
		self.incidents = {}

		self.sessions = {}
		self.change_requests = {}
		self.team_assignment_requests = {}

		self.notes = {}
		self.questions = {}
		self.tasks = {}

		self.notifications = {}

		self.database = database
		self.clearOnStartUp = clearOnStartUp

	def initialize(self):
		def execute_script(filename):
			script = open(filename, "r")
			queries = self.database.parse_queries(script)
			self.database.execute_queries(queries)
			script.close()

		if self.database.connect():
			execute_script("SQL_scripts/create_tables.sql")

		if self.clearOnStartUp:
			print('Cleaning')
			execute_script("SQL_scripts/drop_tables.sql")

		execute_script("SQL_scripts/create_tables.sql")

		if self.database.table_empty("Impact"):
			print("Initializing Impact Table")
			self.create_impact(Impact.IMP1)
			self.create_impact(Impact.IMP2)
			self.create_impact(Impact.IMP3)
		else:
			print("Loading Impact Table")
			self.load_impacts()
			#print(self.impacts)

		if self.database.table_empty("Priority"):
			print("Initializing Priority Table")
			self.create_priority(Priority.P1)
			self.create_priority(Priority.P2)
			self.create_priority(Priority.P3)
		else:
			print("Loading Priority Table")
			self.load_priorities()
			#print(self.priorities)

		if self.database.table_empty("Severity"):
			print("Initializing Severity Table")
			self.create_severity(Severity.S1)
			self.create_severity(Severity.S2)
			self.create_severity(Severity.S3)
		else:
			print("Loading Severity Table")
			self.load_severities()
			#print(self.severities)

		if self.database.table_empty("Stage"):
			print("Initializing Stage Table")
			self.create_stage(Stage.IDENTIFYING)
			self.create_stage(Stage.RESOLVING)
			self.create_stage(Stage.RESOLVED)
		else:
			print("Loading Stage Table")
			self.load_stages()
			#print(self.stages)

		if self.database.table_empty("SystemClassification"):
			print("Initializing SystemClassification Table")
			self.create_system_class(SystemClass.INVESTING, 1)
			self.create_system_class(SystemClass.RETAIL, 1)
			self.create_system_class(SystemClass.TRANSACTION, 1)
			self.create_system_class(SystemClass.FINANCIAL_ANALYSIS, 1)

			self.create_system_class(SystemClass.FINANCIAL_REPORTING, 2)
			self.create_system_class(SystemClass.PAYROLL, 2)
			self.create_system_class(SystemClass.CORPORATE_ACCOUNTING, 2)

			self.create_system_class(SystemClass.SYSTEM_IMPROVEMENT, 3)
			self.create_system_class(SystemClass.CHANGE_MANAGEMENT, 3)
			self.create_system_class(SystemClass.TIMESHEET, 3)
		else:
			print("Loading SystemClassification Table")
			self.load_system_classes()
			#print(self.system_classes)

		if self.database.table_empty("Role"):
			print("Initializing Role Table")
			self.create_role(Role.MAJOR_INCIDENT_MANAGER, True)
			self.create_role(Role.SERVICE_DESK, True)
			self.create_role(Role.QUEUE_MANAGER, False)
			self.create_role(Role.TECHNICIAN, False)
			self.create_role(Role.RESOLVER, False)
			self.create_role(Role.BASIC_USER, False)
		else:
			print("Loading Role Table")
			self.load_roles()
			#print(self.roles)

		if self.database.table_empty("User"):
			print("Initializing User Table")
			self.create_user("Joe", "Biden", "jb@email.com", "jbiden", "password1", self.get_role_by_name(Role.MAJOR_INCIDENT_MANAGER))
			self.create_user("Donald", "Duck", "DoubleD@email.com", "dduck", "password1", self.get_role_by_name(Role.SERVICE_DESK))
			self.create_user("Boris", "Johnson", "BJob@email.com", "bjohnson", "password1", self.get_role_by_name(Role.QUEUE_MANAGER))
			self.create_user("Frederick", "William", "TheGreat@email.com", "fwilliam", "password1", self.get_role_by_name(Role.TECHNICIAN))
			self.create_user("Jim", "Boston", "AgainJ@email.com", "jboston", "password1", self.get_role_by_name(Role.BASIC_USER))
			self.create_user("Alice", "Wonderfill", "AliceWhere@email.com", "awonderfill", "password1", self.get_role_by_name(Role.RESOLVER))
		else:
			print("Loading User Table")
			self.load_users()
			#print(self.users)

		if self.database.table_empty("Department"):
			print("Initializing Department Table")
			self.create_department(Department.GENERAL_MANAGEMENT)
			self.create_department(Department.FINANCIAL_SERVICES)
			self.create_department(Department.HUMAN_RESOURCES)
			self.create_department(Department.IT_SUPPORT)
		else:
			print("Loading Department Table")
			self.load_departments()
			#print(self.departments)

		if self.database.table_empty("Team"):
			print("Initializing Team Table")
			self.create_team(Team.DERIVATIVES, self.get_department_by_name(Department.FINANCIAL_SERVICES))
			self.create_team(Team.INVESTMENT, self.get_department_by_name(Department.FINANCIAL_SERVICES))
			self.create_team(Team.MORTGAGES, self.get_department_by_name(Department.FINANCIAL_SERVICES))
			self.create_team(Team.ADMIN, self.get_department_by_name(Department.GENERAL_MANAGEMENT))
			self.create_team(Team.RECRUITMENT, self.get_department_by_name(Department.HUMAN_RESOURCES))
			self.create_team(Team.TRAINING, self.get_department_by_name(Department.HUMAN_RESOURCES))
			self.create_team(Team.INCIDENT_RESPONSE, self.get_department_by_name(Department.IT_SUPPORT))
			self.create_team(Team.NETWORKING, self.get_department_by_name(Department.IT_SUPPORT))
			self.create_team(Team.MAINTENANCE, self.get_department_by_name(Department.IT_SUPPORT))
		else:
			print("Loading Team Table")
			self.load_teams()
			#print(self.teams)

		if self.database.table_empty("Incident"):
			print("Initializing Incident Table")
			sla_identification_deadline = '02-06-2020 15:28:00'
			sla_implementation_deadline = '03-06-2020 15:28:00'

			self.create_incident('Payroll Server Crashed', 'Server for the payroll system crashed due to an OutOfMemoryException. It is suspected that this is due to the new release from the Internal Software Development Team', \
				self.get_user_by_username('dduck'), TimeUtil.to_datetime(sla_identification_deadline), TimeUtil.to_datetime(sla_implementation_deadline), \
				self.get_stage_by_level(Stage.IDENTIFYING), self.get_system_class_by_name(SystemClass.PAYROLL), self.get_impact_by_level(Impact.IMP1), \
				self.get_priority_by_code(Priority.P1), self.get_severity_by_code(Severity.S1))
		else:
			print("Loading Incident Table")
			self.load_incidents()

		if not self.database.table_empty("IncidentValueChangeRequest"):
			self.load_change_requests()

		if not self.database.table_empty("IncidentTeamAssignmentRequest"):
			self.load_team_assignment_requests()

		if not self.database.table_empty("Notification"):
			self.load_notifications()

		self.database.commit()

	def create_role(self, name, customer_facing):
		role = Role(name, customer_facing)
		self.database.insert_role(role)
		self.roles[role.id] = role
		return role

	def load_roles(self):
		role_rows = self.database.get_roles()
		for role_row in role_rows:
			role = Role(role_row[1], role_row[2])
			role.id = role_row[0]
			self.roles[role.id] = role

	def get_role_by_name(self, name):
		for role in self.roles.values():
			if role.name == name:
				return role
		return None

	def update_user_role(self, user, new_role):
		user.role = new_role
		self.database.update_user_role(user)
		self.users[user.id] = user

		self.database.commit()

	def get_role(self, role_id):
		return self.roles[role_id]

	def get_all_roles(self):
		return list(self.roles.values())

	def create_user(self, forename, surname, email, username, password, role):
		user = User(forename, surname, email, username, password, role)
		self.database.insert_user(user)
		self.users[user.id] = user
		return user

	def load_users(self):
		user_rows = self.database.get_users()
		for user_row in user_rows:
			user = User(user_row[1], user_row[2], \
				user_row[3], user_row[4], user_row[5], \
				self.get_role(user_row[6]))
			user.id = user_row[0]
			self.users[user.id] = user

	def get_users(self):
		return list(self.users.values())

	def get_user_by_username(self, username):
		for user in self.users.values():
			if user.username == username:
				return user
		return None

	def get_user(self, user_id):
		return self.users[user_id]

	def login(self, user):
		if user.id in self.sessions:
			return

		user_session = UserSession(user)
		self.database.insert_user_session(user_session)
		self.sessions[user.id] = user_session

	def logout(self, user):
		if user.id in self.sessions:
			user_session = self.sessions[user.id]
			self.database.update_user_session(user_session)
			del self.sessions[user.id]

	def create_department(self, name):
		department = Department(name)
		self.database.insert_department(department)
		self.departments[department.id] = department
		return department

	def get_department_by_name(self, name):
		for department in self.departments.values():
			if department.name == name:
				return department
		return None

	def get_department(self, department_id):
		return self.departments[department_id]

	def load_departments(self):
		department_rows = self.database.get_departments()
		for department_row in department_rows:
			department = Department(department_row[1])
			department.id = department_row[0]
			self.departments[department.id] = department

	def get_all_departments(self):
		return list(self.departments.values())

	def create_team(self, name, department):
		team = Team(name, department)
		self.database.insert_team(team)
		self.teams[team.id] = team
		return team

	def get_teams(self, department):
		teams = []
		for team in self.teams.values():
			if team.department.id == department.id:
				teams.append(team)
		return teams

	def get_team_by_name(self, name):
		for team in self.teams.values():
			if team.name == name:
				return team
		return None

	def get_team(self, team_id):
		return self.teams[team_id]

	def load_teams(self):
		team_rows = self.database.get_teams()
		for team_row in team_rows:
			team = Team(team_row[1], self.get_department(team_row[2]))
			team.id = team_row[0]
			self.teams[team.id] = team

	def create_impact(self, level):
		impact = Impact(level)
		self.database.insert_impact(impact)
		self.impacts[impact.id] = impact
		return impact

	def get_impact_by_level(self, level):
		for impact in self.impacts.values():
			if impact.level == level:
				return impact
		return None

	def get_impact(self, level):
		return self.impacts[level]

	def load_impacts(self):
		impact_rows = self.database.get_impacts()
		for impact_row in impact_rows:
			impact = Impact(impact_row[1])
			impact.id = impact_row[0]
			self.impacts[impact.id] = impact

	def get_all_impacts(self):
		return list(self.impacts.values())

	def create_priority(self, code):
		priority = Priority(code)
		self.database.insert_priority(priority)
		self.priorities[priority.id] = priority
		return priority

	def get_priority_by_code(self, code):
		for priority in self.priorities.values():
			if priority.code == code:
				return priority
		return None

	def get_priority(self, priority_id):
		return self.priorities[priority_id]

	def load_priorities(self):
		priorities_rows = self.database.get_priorities()
		for priority_row in priorities_rows:
			priority = Priority(priority_row[1])
			priority.id = priority_row[0]
			self.priorities[priority.id] = priority

	def get_all_priorities(self):
		return list(self.priorities.values())

	def create_severity(self, code):
		severity = Severity(code)
		self.database.insert_severity(severity)
		self.severities[severity.id] = severity
		return severity

	def get_severity_by_code(self, code):
		for severity in self.severities.values():
			if severity.code == code:
				return severity
		return None

	def get_severity(self, severity_id):
		return self.severities[severity_id]

	def load_severities(self):
		severities_rows = self.database.get_severities()
		for severity_row in severities_rows:
			severity = Severity(severity_row[1])
			severity.id = severity_row[0]
			self.severities[severity.id] = severity

	def get_all_severities(self):
		return list(self.severities.values())

	def create_stage(self, level):
		stage = Stage(level)
		self.database.insert_stage(stage)
		self.stages[stage.id] = stage
		return stage

	def get_stage_by_level(self, level):
		for stage in self.stages.values():
			if stage.level == level:
				return stage
		return None

	def get_stage(self, stage_id):
		return self.stages[stage_id]

	def load_stages(self):
		stage_rows = self.database.get_stages()
		for stage_row in stage_rows:
			stage = Stage(stage_row[1])
			stage.id = stage_row[0]
			self.stages[stage.id] = stage

	def create_system_class(self, name, tier):
		system_class = SystemClass(name, tier)
		self.database.insert_system_class(system_class)
		self.system_classes[system_class.id] = system_class
		return system_class

	def get_system_class_by_name(self, system_name):
		for system_class in self.system_classes.values():
			if system_class.name == system_name:
				return system_class
		return None

	def get_system_class(self, system_id):
		return self.system_classes[system_id]

	def load_system_classes(self):
		system_class_rows = self.database.get_system_classes()
		for system_class_row in system_class_rows:
			system_class = SystemClass(system_class_row[1], system_class_row[2])
			system_class.id = system_class_row[0]
			self.system_classes[system_class.id] = system_class

	def get_all_system_classes(self):
		return list(self.system_classes.values())

	def create_incident(self, title, description, author, \
			sla_identification_time, sla_implementation_time, \
			status, system, impact, priority, severity):
		incident = Incident(self, title, description, author, sla_identification_time, \
			sla_implementation_time, status, system, impact, priority, severity)
		self.database.insert_incident(incident)

		date_created = self.database.get_incident_create_date(incident)
		incident.date_created = date_created
		self.incidents[incident.id] = incident

		self.database.commit()
		return incident

	def get_incidents(self, author):
		incidents = []
		for incident in list(self.incidents.values()):
			if incident.author.id == author.id:
				incidents.append(incident)
		return incidents

	def load_incidents(self):
		incident_rows = self.database.get_incidents()
		for incident_row in incident_rows:
			author = self.get_user(incident_row[1])
			status = self.get_stage(incident_row[6])
			system = self.get_system_class(incident_row[7])
			impact = self.get_impact(incident_row[8])
			severity = self.get_severity(incident_row[9])
			priority = self.get_priority(incident_row[10])
			sla_identification_deadline = TimeUtil.sqlite_to_datetime(incident_row[4])
			sla_implementation_deadline = TimeUtil.sqlite_to_datetime(incident_row[5])
			incident = Incident(self, incident_row[2], incident_row[3], author, \
				sla_identification_deadline, sla_implementation_deadline, status, system, \
				impact, priority, severity)
			incident.id = incident_row[0]
			incident.date_created = incident_row[11]
			incident.date_identified = incident_row[12]
			incident.date_implemented = incident_row[13]

			note_rows = self.database.get_notes(incident)
			for note_row in note_rows:
				note_id = note_row[0]
				note_title = note_row[1]
				note_author = self.get_user(note_row[2])
				date_created = note_row[3]
				note_content = note_row[4]
				note = Note(note_title, note_author, note_content)
				note.id = note_id
				note.date_created = date_created

				incident.notes.append(note)
				self.notes[note.id] = note

			question_rows = self.database.get_questions(incident)
			for question_row in question_rows:
				question_id = question_row[0]
				question_title = question_row[1]
				question_issuer = self.get_user(question_row[2])
				date_asked = question_row[3]
				question_content = question_row[4]
				question = Question(question_title, question_issuer, question_content)
				question.id = question_id
				question.date_asked = date_asked

				answer_rows = self.database.get_answers(question)
				for answer_row in answer_rows:
					answer_id = answer_row[0]
					answer_answerer = self.get_user(answer_row[1])
					answer_content = answer_row[2]
					date_answered = answer_row[3]
					answer = Answer(question, answer_answerer, answer_content)
					answer.id = answer_id
					answer.date_answered = date_answered

					question.answers.append(answer)

				incident.questions.append(question)
				self.questions[question.id] = question

			task_rows = self.database.get_tasks(incident)
			for task_row in task_rows:
				task_id = task_row[0]
				task_name = task_row[1]
				task_author = self.get_user(task_row[2])
				date_created = task_row[3]
				task_content = task_row[4]
				task_status = task_row[5]
				task = Task(task_name, task_author, task_content, task_status)
				task.id = task_id
				task.date_created = date_created

				task_team_rows = self.database.get_task_team_assignment_requests(task)
				for task_team_row in task_team_rows:
					task_team = self.get_team(task_team_row[0])
					assigner = self.get_user(task_team_row[1])
					status = task_team_row[2]
					date_issued = task_team_row[3]

					assigned_team = AssignedTeam(task_team, task)
					assigned_team.status = status
					assigned_team.date_issued = date_issued

					task.teams.append(assigned_team)

				incident.tasks.append(task)
				self.tasks[task.id] = task

			self.incidents[incident.id] = incident

	def get_incident_of_task(self, task):
		for incident in self.incidents.values():
			tasks = incident.tasks
			for incident_task in tasks:
				if incident_task.id == task.id:
					return incident
		return None

	def request_team_assignment(self, assigner, assigned_to, team):
		team_assignment_request = TeamAssignmentRequest(team, assigned_to, assigner, IncidentValueChangeRequest.STATUS_PENDING)

		if isinstance(assigned_to, Incident):
			assignment_type = 'incident'
			incident = assigned_to
			self.database.insert_team_assignment_request(team_assignment_request)
			print('inserted incident team assignment')
		else:
			assignment_type = 'task'
			incident = self.get_incident_of_task(assigned_to)
			self.database.insert_task_team_assignment_request(team_assignment_request)
			print('inserted task team assignment')

		team_assignment_request.date_issued = self.database.get_assignment_date_requested(team_assignment_request)
		self.create_notification(incident, assigner.forename + ' ' + assigner.surname + ' has request a team assignment on ' + assignment_type + assigned_to.title)

		self.team_assignment_requests[(team_assignment_request.team.id, team_assignment_request.assigned_to.id)] = team_assignment_request

		self.database.commit()
		return team_assignment_request

	def get_team_assignment_requests(self, assigned_to):
		team_assignment_requests = []
		for team_assignment_request in list(self.team_assignment_requests.values()):
			if team_assignment_request.assigned_to.id == assigned_to.id:
				team_assignment_requests.append(team_assignment_request)
		return team_assignment_requests

	def get_team_assignment_request(self, assigned_to, team):
		if isinstance(assigned_to, Incident):
			assignment_type = 'Incident'
		else:
			assignment_type = 'Task'
		return self.team_assignment_requests[(team.id, assigned_to.id, assignment_type)]

	def get_all_team_assignment_requests(self):
		return list(self.team_assignment_requests.values())

	def load_team_assignment_requests(self):
		team_assignment_rows = self.database.get_all_team_assignment_requests()
		for team_assignment_row in team_assignment_rows:
			team = self.get_team(team_assignment_row[0])
			incident = self.get_incident(team_assignment_row[1])
			assigner = self.get_user(team_assignment_row[2])
			status = team_assignment_row[3]
			date_issued = team_assignment_row[4]
			team_assignment_request = TeamAssignmentRequest(team, incident, assigner, status)
			team_assignment_request.date_issued = date_issued

			self.team_assignment_requests[(team.id, incident.id, 'Incident')] = team_assignment_request

		task_team_assignment_rows = self.database.get_all_task_team_assignment_requests()
		for task_team_assignment_row in task_team_assignment_rows:
			print('task team request loaded')
			team = self.get_team(task_team_assignment_row[0])
			task = self.get_task(task_team_assignment_row[1])
			assigner = self.get_user(task_team_assignment_row[2])
			status = task_team_assignment_row[3]
			date_issued = task_team_assignment_row[4]
			team_assignment_request = TeamAssignmentRequest(team, task, assigner, status)
			team_assignment_request.date_issued = date_issued

			self.team_assignment_requests[(team.id, task.id, 'Task')] = team_assignment_request

	def request_value_change(self, user, incident, old_value, new_value, value_type, justification):
		change_request = IncidentValueChangeRequest(user, incident, old_value, new_value, value_type, justification)
		self.database.insert_change_request(change_request)
		change_request.date_requested = self.database.get_date_requested(change_request)
		change_request.status = IncidentValueChangeRequest.STATUS_PENDING
		self.create_notification(incident, user.forename + ' ' + user.surname + ' has requested a ' + IncidentValueChangeRequest.value_type_to_string(value_type) + ' Change on ' + incident.title)

		self.change_requests[change_request.id] = change_request

		self.database.commit()

	def update_change_request(self, user, change_request, new_value, justification):
		change_request.new_value = new_value
		change_request.justification = justification

		self.change_requests[change_request.id] = change_request
		self.database.update_change_request_content(change_request)

		self.create_notification(incident, user.forename + ' ' + user.surname + ' has updated ' + IncidentValueChangeRequest.value_type_to_string(value_type) + ' Change on ' + incident.title)

		self.database.commit()

	def get_change_requests(self, user):
		change_requests = []
		for change_request in list(self.change_requests.values()):
			if change_request.user.id == user.id:
				change_requests.append(change_request)
		return change_requests

	def get_incident_change_requests(self, incident):
		change_requests = []
		for change_request in list(self.change_requests.values()):
			if change_request.incident.id == incident.id:
				change_requests.append(change_request)
		return change_requests

	def get_change_request(self, change_request_id):
		return self.change_requests[change_request_id]

	def get_existing_change_request(self, user, incident, value_type):
		for change_request in list(self.change_requests.values()):
			if change_request.user.id == user.id and change_request.incident.id == incident.id and change_request.value_type == value_type:
				return change_request
		return None

	def get_all_change_requests(self):
		return list(self.change_requests.values())

	def load_change_requests(self):
		change_request_rows = self.database.get_all_change_requests()
		for change_request_row in change_request_rows:
			user = self.get_user(change_request_row[1])
			incident = self.get_incident(change_request_row[2])
			old_value = change_request_row[3]
			new_value = change_request_row[4]
			value_type = change_request_row[5]
			justification = change_request_row[6]
			status = change_request_row[7]
			date_requested = change_request_row[8]
			change_request = IncidentValueChangeRequest(user, incident, old_value, new_value, \
				value_type, justification)
			change_request.id = change_request_row[0]
			change_request.status = status
			change_request.date_requested = date_requested

			self.change_requests[change_request.id] = change_request

	def decide_change_request(self, user, change_request, new_status):
		if change_request.value_type == IncidentValueChangeRequest.TYPE_PRIORITY:
			change_request.incident.priority = self.get_priority_by_code(change_request.new_value)
		elif change_request.value_type == IncidentValueChangeRequest.TYPE_IMPACT:
			change_request.incident.impact = self.get_impact_by_level(change_request.new_value)
		elif change_request.value_type == IncidentValueChangeRequest.TYPE_SEVERITY:
			change_request.incident.severity = self.get_severity_by_code(change_request.new_value)

		self.database.update_incident(change_request.incident)
		self.create_notification(change_request.incident, user.forename + ' ' + user.surname + ' has made a decision on ' + IncidentValueChangeRequest.value_type_to_string(change_request.value_type) + ' Change on ' + change_request.incident.title)

		change_request.status = new_status
		self.change_requests[change_request.id] = change_request
		self.database.update_change_request_status(change_request)

		self.database.commit()

	def update_change_request_content(self, change_request, new_value, justification):
		change_request.new_value = new_value
		change_request.justification = justification

	def get_incident(self, incident_id):
		return self.incidents[incident_id]

	def get_all_incidents(self):
		return list(self.incidents.values())

	def get_assigned_teams(self, incident):
		assigned_teams = []
		assigned_team_rows = self.database.get_assigned_teams(incident)
		for assigned_team_row in assigned_team_rows:
			assigned_team = self.get_team(assigned_team_row[0])
			assigned_team_obj = AssignedTeam(assigned_team, incident)

			team_assignment_details = self.database.get_team_assignment_details(assigned_team_obj)
			assigned_team_obj.assigner = self.get_user(team_assignment_details[0])
			assigned_team_obj.status = team_assignment_details[1]
			assigned_team_obj.date_issued = team_assignment_details[2]

			assigned_teams.append(assigned_team_obj)
		return assigned_teams

	def decide_team_assignment_request(self, user, team_assignment_request, new_status):
		assigned_team = AssignedTeam(team_assignment_request.team, team_assignment_request.assigned_to)
		if isinstance(team_assignment_request.assigned_to, Incident):
			self.database.insert_assigned_team(assigned_team)
		else:
			self.database.insert_task_assigned_team(assigned_team)

		team_assignment_request.status = new_status
		self.team_assignment_requests[(team_assignment_request.team.id, team_assignment_request.assigned_to.id)] = team_assignment_request
		self.database.update_team_assignment_request_status(team_assignment_request)
		self.create_notification(incident, user.forename + ' ' + user.surname + ' has made a decision on a team assignment on ' + incident.title)

		self.database.commit()

	def follow(self, user, incident):
		follow = Follow(user, incident)
		self.database.insert_follow(follow)
		self.create_notification(incident, user.forename + ' ' + user.surname + ' is now following ' + incident.title)

		self.database.commit()

	def is_following(self, user, incident):
		return self.database.execute_query("SELECT * FROM Follow WHERE user_id = ? and incident_id = ?", (user.id, incident.id)) != 0

	def create_note(self, author, incident, title, content):
		note = Note(title, author, content)
		self.database.insert_note(incident, note)
		self.create_notification(incident, author.forename + ' ' + author.surname + ' added a note to ' + incident.title)

		note.date_created = self.database.get_note_date_created(note)

		incident.notes.append(note)
		self.notes[note.id] = note
		self.database.commit()
		return note

	def get_note(self, note_id):
		return self.notes[note_id]

	def create_question(self, author, incident, title, content):
		question = Question(title, author, content)
		self.database.insert_question(incident, question)
		self.create_notification(incident, author.forename + ' ' + author.surname + ' asked a question on ' + incident.title)

		question.date_asked = self.database.get_question_date_asked(question)

		incident.questions.append(question)
		self.questions[question.id] = question
		self.database.commit()
		return question

	def get_question(self, question_id):
		return self.questions[question_id]

	def answer_question(self, answerer, question, answer_content):
		answer = Answer(question, answerer, answer_content)
		self.database.insert_answer(answer)
		self.create_notification(incident, answerer.forename + ' ' + answerer.surname + ' answered a question on ' + incident.title)

		answer.date_answered = self.database.get_date_answered(answer)

		question.answers.append(answer)

		self.database.commit()

	def create_task(self, author, incident, title, content):
		task = Task(title, author, content, "To Do")
		self.database.insert_task(incident, task)

		task.date_created = self.database.get_task_date_created(task)

		incident.tasks.append(task)
		self.database.commit()
		return task

	def get_task(self, task_id):
		return self.tasks[task_id]

	def get_followers(self, incident):
		user_followers = []
		follower_rows = self.database.get_followers(incident)
		for follower in follower_rows:
			user_followers.append(self.get_user(follower[0]))
		return user_followers

	def load_notifications(self):
		notification_rows = self.database.get_notifications()
		for notification_row in notification_rows:
			notification_id = notification_row[0]
			notification_content = notification_row[1]
			date_issued = notification_row[2]
			incident = self.get_incident(notification_row[3])

			notification = Notification(incident, notification_content)
			notification.id = notification_id
			notification.date_issued = date_issued

			self.notifications[notification.id] = notification

	def create_notification(self, incident, content):
		notification = Notification(incident, content)
		self.database.insert_notification(notification)
		self.notifications[notification.id] = notification

		notification.date_issued = self.database.get_notification_date_issued(notification)

		followers = self.get_followers(incident)
		for follower in followers:
			user_notification = UserNotification(follower, notification, False)
			self.database.insert_user_notification(user_notification)

		self.database.commit()

		return notification

	def get_notification(self, notification_id):
		return self.notifications[notification_id]

	def get_notifications_by_incident(self, incident):
		result = []
		for notification in self.notifications.values():
			if notification.incident.id == incident.id:
				result.append(notification)
		return result

	def get_notifications(self, user):
		result = []
		incident_following_rows = self.database.get_incidents_following(user)
		for incident_following_row in incident_following_rows:
			incident = self.get_incident(incident_following_row[0])
			incident_notifications = self.get_notifications_by_incident(incident)
			result.extend(incident_notifications)
		return result

	def get_user_notifications(self, user):
		user_notifications = []
		user_notification_rows = self.database.get_user_notifications(user)
		for user_notification_row in user_notification_rows:
			notification = self.get_notification(user_notification_row[0])
			seen = user_notification_row[1]
			date_notified = user_notification_row[2]
			user_notification = UserNotification(user, notification, seen)
			user_notification.date_notified = date_notified

			user_notifications.append(user_notification)
		return user_notifications

	def seen_user_notification(self, user_notification):
		self.database.seen_user_notification(user_notification)

	def get_on_behalf(self, incident):
		on_behalf = self.database.get_on_behalf(incident)
		if on_behalf is None:
			return None

		on_behalf_user = self.get_user(on_behalf)
		return on_behalf_user

	def update_incident_identified_date(self, user, incident):
		incident.status = self.get_stage_by_level(Stage.RESOLVING)
		self.database.update_incident_identified_date(incident)
		incident.date_identified = self.database.get_incident_identified_date(incident)
		self.create_notification(incident, user.forename + ' ' + user.surname + ' has changed ' + incident.title + '\'s status to ' + incident.status.level)

		self.database.commit()

	def update_incident_implemented_date(self, user, incident):
		incident.status = self.get_stage_by_level(Stage.RESOLVED)
		self.database.update_incident_implemented_date(incident)
		incident.date_implemented = self.database.get_incident_identified_date(incident)
		self.create_notification(incident, user.forename + ' ' + user.surname + ' has changed ' + incident.title + '\'s status to ' + incident.status.level)

		self.database.commit()

	def dump(self):
		print('Roles: ' + str(self.roles))
		print('Users: ' + str(self.users))
		print('Departments: ' + str(self.departments))
		print('Teams: ' + str(self.teams))
