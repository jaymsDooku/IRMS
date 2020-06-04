class Notification:

	def __init__(self, incident, content):
		self.incident = incident
		self.content = content

	def to_sql(self):
		return (self.incident.id, self.content)