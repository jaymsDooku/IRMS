import sqlite3
from sqlite3 import Error

from os import path

class Database:

	def __init__(self, filename):
		self.file = filename

	def connect(self):
		try:
			first_time = (not path.exists(self.file))
			self.connection = sqlite3.connect(self.file)
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

	def execute_query(self, query):
		try:
			cur = self.connection.cursor()
			cur.execute(query)
		except Error as e:
			print(e)

	def execute_queries(self, queries):
		if not self.is_connected():
			return

		for query in queries:
			self.execute_query(query)

	def insert(self, sql, obj):
		cur = self.connection.cursor()
		cur.execute(sql, obj.to_sql())
		obj.id = cur.lastrowid

	def insert_role(self, role):
		self.insert("INSERT INTO Role(role_name, is_customer_facing) VALUES (?, ?)", role)

	def insert_user(self, user):
		self.insert("INSERT INTO User(forename, surname, email, username, password, role) VALUES (?, ?, ?, ?, ?, ?)", user)

	def insert_department(self, department):
		self.insert("INSERT INTO Department(department_name) VALUES (?)", department)

	def insert_team(self, team):
		self.insert("INSERT INTO Team(team_name, department_id) VALUES (?, ?)", team)

	def table_empty(self, table):
		cur = self.connection.cursor()
		cur.execute("SELECT * FROM " + table + " LIMIT 1")
		return cur.rowcount == -1
