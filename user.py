class User:

	def __init__(self, forename, surname, email, username, password, role):
		self.forename = forename
		self.surname = surname
		self.email = email
		self.username = username
		self.password = password
		self.role = role

	def to_sql(self):
		return (self.forename, self.surname, self.email, self.username, self.password, self.role.id)