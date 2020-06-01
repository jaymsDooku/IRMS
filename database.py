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
			rowcount = cur.rowcount
			return rowcount
		except Error as e:
			print(e)

	def execute_queries(self, queries):
		if not self.is_connected():
			return

		for query in queries:
			self.execute_query(query)

	def execute_update(self, sql, obj):
		cur = self.connection.cursor()
		cur.execute(sql, obj.to_sql())
		obj.id = cur.lastrowid

	def insert_role(self, role):
		self.execute_update("INSERT INTO Role(role_name, is_customer_facing) VALUES (?, ?)", role)

	def insert_user(self, user):
		self.execute_update("INSERT INTO User(forename, surname, email, username, password, role) VALUES (?, ?, ?, ?, ?, ?)", user)

	def insert_department(self, department):
		self.execute_update("INSERT INTO Department(department_name) VALUES (?)", department)

	def insert_team(self, team):
		self.execute_update("INSERT INTO Team(team_name, department_id) VALUES (?, ?)", team)

	def insert_impact(self, impact):
		self.execute_update("INSERT INTO Impact(impact_level) VALUES (?)", impact)

	def insert_priority(self, priority):
		self.execute_update("INSERT INTO Priority(priority_code) VALUES (?)", priority)

	def insert_stage(self, stage):
		self.execute_update("INSERT INTO Stage(stage_level) VALUES (?)", stage)

	def insert_system_class(self, system_class):
		self.execute_update("INSERT INTO SystemClassification(system_name, tier) VALUES (?, ?)", system_class)

	def insert_incident(self, incident):
		self.execute_update("INSERT INTO Incident(title, description, author, \
			sla_identification_time_frame, sla_implementation_time_frame, status, \
			system, impact, priority) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", incident)

	def get_incident_create_date(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_created, 'localtime') FROM incident WHERE incident_id = ?", (incident.id, ))
		row = cur.fetchone()
		return row[0]

	def insert_user_session(self, user_session):
		self.execute_update("INSERT INTO UserSession(user_id) VALUES (?)", user_session)

	def update_user_session(self, user_session):
		self.execute_update("UPDATE UserSession SET session_end = DATETIME('now') WHERE user_id = ?", user_session)

	def table_empty(self, table):
		return self.execute_query("SELECT * FROM " + table + " LIMIT 1") == -1
		
