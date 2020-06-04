
class IncidentValueChangeRequest:

	TYPE_PRIORITY = 1
	TYPE_IMPACT = 2
	TYPE_SEVERITY = 3

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
		return IncidentValueChangeRequest.value_type_to_string(self.value_type)

	def get_status(self):
		if self.status is None:
			return None

		return IncidentValueChangeRequest.status_to_string(self.status)

	def to_sql(self):
		return (self.user.id, self.incident.id, self.old_value, self.new_value, self.value_type, self.justification)

	@staticmethod
	def status_to_string(status):
		if status == IncidentValueChangeRequest.STATUS_PENDING:
			return "Pending Review"
		elif status == IncidentValueChangeRequest.STATUS_DENIED:
			return "Denied"
		elif status == IncidentValueChangeRequest.STATUS_APPROVED:
			return "Approved"
		else:
			return None

	@staticmethod
	def value_type_to_string(value_type):
		if value_type == IncidentValueChangeRequest.TYPE_PRIORITY:
			return "Priority"
		elif value_type == IncidentValueChangeRequest.TYPE_IMPACT:
			return "Impact"
		elif value_type == IncidentValueChangeRequest.TYPE_SEVERITY:
			return "Severity"
		else:
			return None

	@staticmethod
	def string_to_value_type(string):
		if string.lower() == "priority":
			return IncidentValueChangeRequest.TYPE_PRIORITY
		elif string.lower() == "impact":
			return IncidentValueChangeRequest.TYPE_IMPACT
		elif string.lower() == "severity":
			return IncidentValueChangeRequest.TYPE_SEVERITY
		else:
			return None