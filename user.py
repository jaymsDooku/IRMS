class User:

	def __init__(self, forename, surname, email, role):
		self.forename = forename
		self.surname = surname
		self.email = email
		self.role = role

	def to_sql(self):
		return (self.forename, self.surname, self.email, self.role.id)