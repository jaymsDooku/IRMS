class Follow:

	def __init__(self, user, incident):
		self.user = user
		self.incident = incident

	def to_sql(self):
		return (self.user.id, self.incident.id)