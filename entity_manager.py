from role import Role
from user import User
from department import Department
from team import Team
from impact import Impact
from priority import Priority
from stage import Stage
from system_class import SystemClass
from incident import Incident
from user_session import UserSession
from incident_value_change_request import IncidentValueChangeRequest
from team_assignment_request import TeamAssignmentRequest

from time_unit import TimeUtil, TimeUnit

class EntityManager:

	def __init__(self, database, clearOnStartUp):
		self.impacts = {}
		self.priorities = {}
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
			self.create_priority(Priority.S1)
			self.create_priority(Priority.S2)
			self.create_priority(Priority.S3)
		else:
			print("Loading Priority Table")
			self.load_priorities()
			#print(self.priorities)

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
				self.get_priority_by_code(Priority.P1))
		else:
			print("Loading Incident Table")
			self.load_incidents()

		if not self.database.table_empty("IncidentValueChangeRequest"):
			self.load_change_requests()

		if not self.database.table_empty("IncidentTeamAssignmentRequest"):
			self.load_team_assignment_requests()

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

	def get_role(self, role_id):
		return self.roles[role_id]

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
			status, system, impact, priority):
		incident = Incident(self, title, description, author, sla_identification_time, \
			sla_implementation_time, status, system, impact, priority)
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
			priority = self.get_priority(incident_row[9])
			sla_identification_deadline = TimeUtil.sqlite_to_datetime(incident_row[4])
			sla_implementation_deadline = TimeUtil.sqlite_to_datetime(incident_row[5])
			incident = Incident(self, incident_row[2], incident_row[3], author, \
				sla_identification_deadline, sla_implementation_deadline, status, system, \
				impact, priority)
			incident.id = incident_row[0]
			incident.date_created = incident_row[10]
			self.incidents[incident.id] = incident

	def request_team_assignment(self, assigner, incident, team):
		team_assignment_request = TeamAssignmentRequest(team, incident, assigner, IncidentValueChangeRequest.STATUS_PENDING)
		self.database.insert_team_assignment_request(team_assignment_request)
		team_assignment_request.date_issued = self.database.get_assignment_date_requested(team_assignment_request)

		self.team_assignment_requests[(team_assignment_request.team.id, team_assignment_request.assigned_to.id)] = team_assignment_request

		self.database.commit()
		return team_assignment_request

	def get_team_assignment_requests(self, assigned_to):
		team_assignment_requests = []
		for team_assignment_request in list(self.team_assignment_requests.values()):
			if team_assignment_request.assigned_to.id == assigned_to.id:
				team_assignment_requests.append(team_assignment_request)
		return team_assignment_requests

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

			self.team_assignment_requests[(team.id, incident.id)] = team_assignment_request

	def request_value_change(self, user, incident, old_value, new_value, value_type, justification):
		change_request = IncidentValueChangeRequest(user, incident, old_value, new_value, value_type, justification)
		self.database.insert_change_request(change_request)
		change_request.date_requested = self.database.get_date_requested(change_request)
		change_request.status = IncidentValueChangeRequest.STATUS_PENDING

		self.change_requests[change_request.id] = change_request

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

	def decide_change_request(self, change_request, new_status):
		if change_request.value_type == IncidentValueChangeRequest.TYPE_PRIORITY:
			change_request.incident.priority = self.get_priority_by_code(change_request.new_value)
		elif change_request.value_type == IncidentValueChangeRequest.TYPE_IMPACT:
			change_request.incident.impact = self.get_impact_by_level(change_request.new_value)
		self.database.update_incident(change_request.incident)

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
			assigned_team = self.get_team(assigned_team_row)
			assigned_team_obj = AssignedTeam(assigned_team, incident)

			team_assigment_details = self.database.get_team_assignment_details(assigned_team_obj)
			assigned_team_obj.assigner = self.get_user(team_assigment_details[0])
			assigned_team_obj.approved = team_assigment_details[1]
			assigned_team_obj.date_issued = team_assigment_details[2]

			assigned_teams.append(assigned_team_obj)
		return assigned_teams

	def is_following(self, user, incident):
		return self.database.execute_query("SELECT * FROM Follow WHERE user_id = ? and incident_id = ?", (user.id, incident.id)) != 0

	def dump(self):
		print('Roles: ' + str(self.roles))
		print('Users: ' + str(self.users))
		print('Departments: ' + str(self.departments))
		print('Teams: ' + str(self.teams))
		print('')
