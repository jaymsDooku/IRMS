from role import Role

class User:

	def __init__(self, forename, surname, email, username, password, role):
		self.forename = forename
		self.surname = surname
		self.email = email
		self.username = username
		self.password = password
		self.role = role

	def has_priority_access(self):
		return True

	def has_severity_access(self):
		return self.role.name == Role.RESOLVER or self.role.name == Role.QUEUE_MANAGER or self.role.name == Role.MAJOR_INCIDENT_MANAGER

	def has_impact_access(self):
		return self.role.name == Role.RESOLVER or self.role.name == Role.QUEUE_MANAGER or self.role.name == Role.MAJOR_INCIDENT_MANAGER

	def has_identified_access(self):
		return self.role.name == Role.RESOLVER or self.role.name == Role.QUEUE_MANAGER or self.role.name == Role.MAJOR_INCIDENT_MANAGER

	def has_implemented_access(self):
		return self.role.name == Role.RESOLVER or self.role.name == Role.QUEUE_MANAGER or self.role.name == Role.MAJOR_INCIDENT_MANAGER

	def to_sql(self):
		return (self.forename, self.surname, self.email, self.username, self.password, self.role.id)