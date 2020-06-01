from role import Role
from user import User
from department import Department
from team import Team
from impact import Impact
from priority import Priority
from stage import Stage
from system_class import SystemClass
from incident import Incident

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
		self.database = database
		self.clearOnStartUp = clearOnStartUp

	def initialize(self):
		def execute_script(filename):
			script = open(filename, "r")
			queries = self.database.parse_queries(script)
			self.database.execute_queries(queries)
			script.close()

		self.database.connect()

		if self.clearOnStartUp:
			execute_script("SQL_scripts/drop_tables.sql")
			execute_script("SQL_scripts/create_tables.sql")

		if self.database.table_empty("Impact"):
			self.create_impact(Impact.IMP1)
			self.create_impact(Impact.IMP2)
			self.create_impact(Impact.IMP3)

		if self.database.table_empty("Priority"):
			self.create_priority(Priority.P1)
			self.create_priority(Priority.P2)
			self.create_priority(Priority.P3)
			self.create_priority(Priority.S1)
			self.create_priority(Priority.S2)
			self.create_priority(Priority.S3)

		if self.database.table_empty("Stage"):
			self.create_stage(Stage.IDENTIFYING)
			self.create_stage(Stage.RESOLVING)
			self.create_stage(Stage.RESOLVED)

		if self.database.table_empty("SystemClassification"):
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

		if self.database.table_empty("Role"):
			print("Initializing Role Table")
			self.create_role(Role.MAJOR_INCIDENT_MANAGER, True)
			self.create_role(Role.SERVICE_DESK, True)
			self.create_role(Role.QUEUE_MANAGER, False)
			self.create_role(Role.TECHNICIAN, False)
			self.create_role(Role.RESOLVER, False)
			self.create_role(Role.BASIC_USER, False)

		if self.database.table_empty("User"):
			print("Initializing User Table")
			self.create_user("Joe", "Biden", "jb@email.com", "jbiden", "password1", self.get_role(Role.MAJOR_INCIDENT_MANAGER))
			self.create_user("Donald", "Duck", "DoubleD@email.com", "dduck", "password1", self.get_role(Role.SERVICE_DESK))
			self.create_user("Boris", "Johnson", "BJob@email.com", "bjohnson", "password1", self.get_role(Role.QUEUE_MANAGER))
			self.create_user("Frederick", "William", "TheGreat@email.com", "fwilliam", "password1", self.get_role(Role.TECHNICIAN))
			self.create_user("Jim", "Boston", "AgainJ@email.com", "jboston", "password1", self.get_role(Role.BASIC_USER))
			self.create_user("Alice", "Wonderfill", "AliceWhere@email.com", "awonderfill", "password1", self.get_role(Role.RESOLVER))

		if self.database.table_empty("Department"):
			print("Initializing Department Table")
			self.create_department(Department.GENERAL_MANAGEMENT)
			self.create_department(Department.FINANCIAL_SERVICES)
			self.create_department(Department.HUMAN_RESOURCES)
			self.create_department(Department.IT_SUPPORT)

		if self.database.table_empty("Team"):
			print("Initializing Team Table")
			self.create_team(Team.DERIVATIVES, self.get_department(Department.FINANCIAL_SERVICES))
			self.create_team(Team.INVESTMENT, self.get_department(Department.FINANCIAL_SERVICES))
			self.create_team(Team.MORTGAGES, self.get_department(Department.FINANCIAL_SERVICES))
			self.create_team(Team.ADMIN, self.get_department(Department.GENERAL_MANAGEMENT))
			self.create_team(Team.RECRUITMENT, self.get_department(Department.HUMAN_RESOURCES))
			self.create_team(Team.TRAINING, self.get_department(Department.HUMAN_RESOURCES))
			self.create_team(Team.INCIDENT_RESPONSE, self.get_department(Department.IT_SUPPORT))
			self.create_team(Team.NETWORKING, self.get_department(Department.IT_SUPPORT))
			self.create_team(Team.MAINTENANCE, self.get_department(Department.IT_SUPPORT))

		if self.database.table_empty("Incident"):
			print("Initializing Incident Table")
			self.create_incident('Payroll Server Crashed', 'Server for the payroll system crashed due to an OutOfMemoryException. It is suspected that this is due to the new release from the Internal Software Development Team', \
				self.get_user_by_username('dduck'), TimeUtil.to_millis(2, TimeUnit.HOUR), TimeUtil.to_millis(1, TimeUnit.DAY), \
				self.get_stage(Stage.IDENTIFYING), self.get_system_class(SystemClass.PAYROLL), self.get_impact(Impact.IMP1), \
				self.get_priority(Priority.P1))

		self.database.commit()

	def create_role(self, name, customer_facing):
		role = Role(name, customer_facing)
		self.database.insert_role(role)
		self.roles[role.id] = role
		return role

	def get_role(self, name):
		for role in self.roles.values():
			if role.name == name:
				return role
		return None

	def create_user(self, forename, surname, email, username, password, role):
		user = User(forename, surname, email, username, password, role)
		self.database.insert_user(user)
		self.users[user.id] = user
		return user

	def get_user_by_username(self, username):
		for user in self.users.values():
			if user.username == username:
				return user
		return None

	def get_user(self, user_id):
		return self.users[user_id]

	def login(self, user):
		self.database.insert_user_session((user.id, ))

	def logout(self, user):
		self.database.update_user_session((user.id, ))

	def create_department(self, name):
		department = Department(name)
		self.database.insert_department(department)
		self.departments[department.id] = department
		return department

	def get_department(self, name):
		for department in self.departments.values():
			if department.name == name:
				return department
		return None

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

	def get_team(self, name):
		for team in self.teams.values():
			if team.name == name:
				return team
		return None

	def create_impact(self, level):
		impact = Impact(level)
		self.database.insert_impact(impact)
		self.impacts[impact.id] = impact
		return impact

	def get_impact(self, level):
		for impact in self.impacts.values():
			if impact.level == level:
				return impact
		return None

	def get_all_impacts(self):
		return list(self.impacts.values())

	def create_priority(self, code):
		priority = Priority(code)
		self.database.insert_priority(priority)
		self.priorities[priority.id] = priority
		return priority

	def get_priority(self, code):
		for priority in self.priorities.values():
			if priority.code == code:
				return priority
		return None

	def get_all_priorities(self):
		return list(self.priorities.values())

	def create_stage(self, level):
		stage = Stage(level)
		self.database.insert_stage(stage)
		self.stages[stage.id] = stage
		return stage

	def get_stage(self, level):
		for stage in self.stages.values():
			if stage.level == level:
				return stage
		return None

	def create_system_class(self, name, tier):
		system_class = SystemClass(name, tier)
		self.database.insert_system_class(system_class)
		self.system_classes[system_class.id] = system_class
		return system_class

	def get_system_class(self, system_name):
		for system_class in self.system_classes.values():
			if system_class.name == system_name:
				return system_class
		return None

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
		return incident

	def get_incidents(self, author):
		incidents = []
		for incident in list(self.incidents.values()):
			if incident.author.id == author.id:
				incidents.append(incident)
		return incidents

	def get_all_incidents(self):
		return list(self.incidents.values())

	def is_following(self, user, incident):
		return self.database.execute_query("SELECT * FROM Follow WHERE user_id = ? and incident_id = ?", (user.id, incident.id)) != -1

	def dump(self):
		print('Roles: ' + str(self.roles))
		print('Users: ' + str(self.users))
		print('Departments: ' + str(self.departments))
		print('Teams: ' + str(self.teams))
