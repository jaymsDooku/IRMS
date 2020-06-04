from incident_value_change_request import IncidentValueChangeRequest

class AssignedTeam():

	def __init__(self, team, assigned_to):
		self.team = team
		self.assigned_to = assigned_to

	def get_status(self):
		return IncidentValueChangeRequest.status_to_string(self.status)

	def to_sql(self):
		return (self.team.id, self.assigned_to.id)