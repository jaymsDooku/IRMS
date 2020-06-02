from incident_value_change_request import IncidentValueChangeRequest

class AssignedTeam():

	def __init__(self, team, incident):
		self.team = team
		self.incident = incident

	def get_status(self):
		return IncidentValueChangeRequest.status_to_string(self.status)

	def to_sql(self):
		return (self.team.id, self.incident.id)