from role import Role
from user import User
from department import Department
from team import Team

class EntityManager:

	def __init__(self, database, clearOnStartUp):
		self.roles = {}
		self.users = {}
		self.departments = {}
		self.teams = {}
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

	def create_team(self, name, department):
		team = Team(name, department)
		self.database.insert_team(team)
		self.teams[team.id] = team
		return team

	def dump(self):
		print('Roles: ' + str(self.roles))
		print('Users: ' + str(self.users))
		print('Departments: ' + str(self.departments))
		print('Teams: ' + str(self.teams))
