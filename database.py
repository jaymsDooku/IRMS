import sqlite3
from sqlite3 import Error

from os import path

class Database:

	def __init__(self, filename):
		self.file = filename

	def connect(self):
		try:
			first_time = (not path.exists(self.file))
			self.connection = sqlite3.connect(self.file, check_same_thread=False)
			return first_time
		except Error as e:
			print(e)

	def commit(self):
		if self.connection:
			self.connection.commit()

	def close(self):
		if self.connection:
			self.connection.close()

	def is_connected(self):
		return self.connection is not None

	def parse_queries(self, script):
		queries = []
		current_query = ""
		for line in script:
			current_query += line
			if ';' in line:
				queries.append(current_query)
				current_query = ""
		return queries

	def execute_query(self, query, obj = None):
		try:
			cur = self.connection.cursor()
			if obj is None:
				cur.execute(query)
			else:
				cur.execute(query, obj)
			return len(cur.fetchall())
		except Error as e:
			print(e)

	def execute_queries(self, queries):
		if not self.is_connected():
			return

		for query in queries:
			self.execute_query(query)

	def execute_update(self, sql, obj):
		try:
			cur = self.connection.cursor()
			cur.execute(sql, obj.to_sql())
			obj.id = cur.lastrowid
		except Error as e:
			print(e)

	def insert_role(self, role):
		self.execute_update("INSERT INTO Role(role_name, is_customer_facing) VALUES (?, ?)", role)

	def get_roles(self):
		cur = self.connection.cursor()
		cur.execute("SELECT role_id, role_name, is_customer_facing FROM Role")
		rows = cur.fetchall()
		return rows

	def insert_user(self, user):
		self.execute_update("INSERT INTO User(forename, surname, email, username, password, role) VALUES (?, ?, ?, ?, ?, ?)", user)

	def get_users(self):
		cur = self.connection.cursor()
		cur.execute("SELECT user_id, forename, surname, email, username, password, role FROM User")
		rows = cur.fetchall()
		return rows

	def insert_department(self, department):
		self.execute_update("INSERT INTO Department(department_name) VALUES (?)", department)

	def get_departments(self):
		cur = self.connection.cursor()
		cur.execute("SELECT department_id, department_name FROM Department")
		rows = cur.fetchall()
		return rows		

	def insert_team(self, team):
		self.execute_update("INSERT INTO Team(team_name, department_id) VALUES (?, ?)", team)

	def get_teams(self):
		cur = self.connection.cursor()
		cur.execute("SELECT team_id, team_name, department_id FROM Team")
		rows = cur.fetchall()
		return rows

	def insert_impact(self, impact):
		self.execute_update("INSERT INTO Impact(impact_level) VALUES (?)", impact)

	def get_impacts(self):
		cur = self.connection.cursor()
		cur.execute("SELECT impact_id, impact_level FROM Impact")
		rows = cur.fetchall()
		return rows

	def insert_priority(self, priority):
		self.execute_update("INSERT INTO Priority(priority_code) VALUES (?)", priority)

	def get_priorities(self):
		cur = self.connection.cursor()
		cur.execute("SELECT priority_id, priority_code FROM Priority")
		rows = cur.fetchall()
		return rows

	def insert_stage(self, stage):
		self.execute_update("INSERT INTO Stage(stage_level) VALUES (?)", stage)

	def get_stages(self):
		cur = self.connection.cursor()
		cur.execute("SELECT stage_id, stage_level FROM Stage")
		rows = cur.fetchall()
		return rows

	def insert_system_class(self, system_class):
		self.execute_update("INSERT INTO SystemClassification(system_name, tier) VALUES (?, ?)", system_class)

	def get_system_classes(self) :
		cur = self.connection.cursor()
		cur.execute("SELECT system_classification_id, system_name, tier FROM SystemClassification")
		rows = cur.fetchall()
		return rows

	def insert_incident(self, incident):
		self.execute_update("INSERT INTO Incident(title, description, author, \
			sla_identification_deadline, sla_implementation_deadline, status, \
			system, impact, priority) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", incident)

	def get_incidents(self):
		cur = self.connection.cursor()
		cur.execute("SELECT author, title, description, sla_identification_deadline, \
			sla_implementation_deadline, status, system, impact, priority, date_created \
			FROM Incident")
		rows = cur.fetchall()
		return rows

	def get_incident_create_date(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_created, 'localtime') FROM Incident WHERE incident_id = ?", (incident.id, ))
		row = cur.fetchone()
		return row[0]

	def get_assigned_teams(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT team_id FROM IncidentTeamAssignment WHERE incident_id = ?", (incident.id, ))
		rows = cur.fetchall()
		return rows

	def get_team_assignment_details(self, assigned_team):
		cur = self.connection.cursor()
		cur.execute("SELECT request_issuer, approved, date_issued FROM IncidentTeamAssignmentRequest WHERE team_id = ? AND incident_id = ?", (assigned_team.team.id, assigned_team.incident.id))
		row = cur.fetchone()
		return row[0]

	def insert_user_session(self, user_session):
		self.execute_update("INSERT INTO UserSession(user_id) VALUES (?)", user_session)

	def update_user_session(self, user_session):
		self.execute_update("UPDATE UserSession SET session_end = DATETIME('now') WHERE user_id = ?", user_session)

	def table_empty(self, table):
		query = "SELECT * FROM " + table + " LIMIT 1"
		return self.execute_query(query) == 0
		
