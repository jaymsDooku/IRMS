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

	def update_incident(self, incident):
		cur = self.connection.cursor()
		cur.execute("UPDATE Incident SET priority = ?, impact = ?, status = ? WHERE incident_id = ?", (incident.priority.id, incident.impact.id, incident.status.id, incident.id))

	def get_incidents(self):
		cur = self.connection.cursor()
		cur.execute("SELECT incident_id, author, title, description, sla_identification_deadline, \
			sla_implementation_deadline, status, system, impact, priority, date_created \
			FROM Incident")
		rows = cur.fetchall()
		return rows

	def get_incident_create_date(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_created, 'localtime') FROM Incident WHERE incident_id = ?", (incident.id, ))
		row = cur.fetchone()
		return row[0]

	def insert_assigned_team(self, assigned_team):
		self.execute_update("INSERT INTO IncidentTeamAssignment(team_id, incident_id) VALUES (?, ?)", assigned_team)

	def get_assigned_teams(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT team_id FROM IncidentTeamAssignment WHERE incident_id = ?", (incident.id, ))
		rows = cur.fetchall()
		return rows

	def get_team_assignment_details(self, assigned_team):
		cur = self.connection.cursor()
		cur.execute("SELECT request_issuer, status, date_issued FROM IncidentTeamAssignmentRequest WHERE team_id = ? AND incident_id = ?", (assigned_team.team.id, assigned_team.incident.id))
		row = cur.fetchone()
		return row

	def insert_team_assignment_request(self, team_assignment_request):
		self.execute_update("INSERT INTO IncidentTeamAssignmentRequest(team_id, incident_id, request_issuer, status) VALUES (?, ?, ?, ?)", team_assignment_request)

	def get_assignment_date_requested(self, team_assignment_request):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_issued, 'localtime') FROM IncidentTeamAssignmentRequest WHERE team_id = ? AND incident_id = ?", (team_assignment_request.team.id, team_assignment_request.assigned_to.id))
		row = cur.fetchone()
		return row[0]

	def get_all_team_assignment_requests(self):
		cur = self.connection.cursor()
		cur.execute("SELECT team_id, incident_id, request_issuer, status, date_issued \
			FROM IncidentTeamAssignmentRequest")
		rows = cur.fetchall()
		return rows

	def update_team_assignment_request_status(self, team_assignment_request):
		cur = self.connection.cursor()
		cur.execute("UPDATE IncidentTeamAssignmentRequest SET status = ? WHERE team_id = ? AND incident_id = ?", (team_assignment_request.status, team_assignment_request.team.id, team_assignment_request.assigned_to.id))

	def insert_change_request(self, change_request):
		self.execute_update("INSERT INTO IncidentValueChangeRequest(user_id, incident_id, old_value, new_value, value_type, justification) VALUES (?, ?, ?, ?, ?, ?)", change_request)

	def update_change_request_status(self, change_request):
		cur = self.connection.cursor()
		print('status: ' + str(change_request.status))
		print('id: ' + str(change_request.id))
		cur.execute("UPDATE IncidentValueChangeRequest SET status = ? WHERE change_request_id = ?", (change_request.status, change_request.id))

	def update_change_request_content(self, change_request):
		cur = self.connection.cursor()
		cur.execute("UPDATE IncidentValueChangeRequest SET new_value = ?, justification = ? WHERE user_id = ? AND incident_id = ? AND value_type = ?", (change_request.new_value, change_request.justification, \
			change_request.user.id, change_request.incident.id, change_request.value_type))

	def get_all_change_requests(self):
		cur = self.connection.cursor()
		cur.execute("SELECT change_request_id, user_id, incident_id, old_value, new_value, value_type, justification, status, date_requested \
			FROM IncidentValueChangeRequest")
		rows = cur.fetchall()
		return rows

	def get_date_requested(self, change_request):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_requested, 'localtime') FROM IncidentValueChangeRequest WHERE user_id = ? AND incident_id = ?", (change_request.user.id, change_request.incident.id))
		row = cur.fetchone()
		return row[0]

	def insert_user_session(self, user_session):
		self.execute_update("INSERT INTO UserSession(user_id) VALUES (?)", user_session)

	def update_user_session(self, user_session):
		self.execute_update("UPDATE UserSession SET session_end = DATETIME('now') WHERE user_id = ?", user_session)

	def insert_note(self, incident, note):
		cur = self.connection.cursor()
		cur.execute("INSERT INTO Note(incident_id, note_title, author, note_content) VALUES (?, ?, ?, ?)", (incident.id, note.title, note.author.id, note.content))
		note.id = cur.lastrowid

	def insert_question(self, incident, question):
		cur = self.connection.cursor()
		cur.execute("INSERT INTO Question(incident_id, question_title, issuer, question_content) VALUES (?, ?, ?, ?)", (incident.id, question.title, question.author.id, question.content))
		question.id = cur.lastrowid

	def insert_task(self, incident, task):
		cur = self.connection.cursor()
		cur.execute("INSERT INTO Task(incident_id, name, author, content, status) VALUES (?, ?, ?, ?, ?)", (incident.id, task.title, task.author.id, task.content, task.status))
		task.id = cur.lastrowid

	def get_notes(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT note_id, note_title, author, date_created, note_content FROM Note WHERE incident_id = ?", (incident.id, ))
		rows = cur.fetchall()
		return rows

	def get_note_date_created(self, note):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_created, 'localtime') FROM Note WHERE note_id = ?", (note.id, ))
		row = cur.fetchone()
		return row[0]

	def get_questions(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT question_id, question_title, issuer, date_asked, question_content FROM Question WHERE incident_id = ?", (incident.id, ))
		rows = cur.fetchall()
		return rows

	def get_question_date_asked(self, question):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_asked, 'localtime') FROM Question WHERE question_id = ?", (question.id, ))
		row = cur.fetchone()
		return row[0]

	def get_tasks(self, incident):
		cur = self.connection.cursor()
		cur.execute("SELECT task_id, name, author, date_created, content, status FROM Task WHERE incident_id = ?", (incident.id, ))
		rows = cur.fetchall()
		return rows

	def get_task_date_created(self, task):
		cur = self.connection.cursor()
		cur.execute("SELECT DATETIME(date_created, 'localtime') FROM Task WHERE task_id = ?", (task.id, ))
		row = cur.fetchone()
		return row[0]

	def table_empty(self, table):
		query = "SELECT * FROM " + table + " LIMIT 1"
		return self.execute_query(query) == 0
		
