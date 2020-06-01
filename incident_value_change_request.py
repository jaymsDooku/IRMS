
class IncidentValueChangeRequest:

	TYPE_PRIORITY = 1
	TYPE_IMPACT = 2

	STATUS_PENDING = -1
	STATUS_DENIED = 0
	STATUS_APPROVED = 1

	def __init__(self, user, incident, old_value, new_value, value_type, justification):
		self.user = user
		self.incident = incident
		self.old_value = old_value
		self.new_value = new_value
		self.value_type = value_type
		self.justification = justification

	def get_value_type(self):
		return IncidentValueChangeRequest.get_value_type(self.value_type)

	def get_status(self):
		if self.status is None:
			return None

		return IncidentValueChangeRequest.get_status(self.status)

	def to_sql(self):
		return (self.user.id, self.incident.id, self.old_value, self.new_value, self.value_type, self.justification)

	@staticmethod
	def get_status(status):
		if status == STATUS_PENDING:
			return "Pending Review"
		elif status == STATUS_DENIED:
			return "Denied"
		elif status == STATUS_APPROVED:
			return "Approved"
		else:
			return None

	@staticmethod
	def get_value_type(value_type):
		if value_type == TYPE_PRIORITY:
			return "Priority"
		elif value_type == TYPE_IMPACT:
			return "Impact"
		else:
			return None