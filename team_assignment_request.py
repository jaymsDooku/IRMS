from task import Task
from incident_value_change_request import IncidentValueChangeRequest

class TeamAssignmentRequest:

	def __init__(self, entity_manager, team, assigned_to, assigner, status):
		self.em = entity_manager
		self.team = team
		self.assigned_to = assigned_to
		self.assigner = assigner
		self.status = status

	def get_status(self):
		return IncidentValueChangeRequest.status_to_string(self.status)

	def get_assigned_type(self):
		if isinstance(self.assigned_to, Task):
			return "Task"
		else:
			return "Incident"

	def get_incident_id(self):
		if isinstance(self.assigned_to, Task):
			return self.em.get_incident_by_task(self.assigned_to).id
		else:
			return self.assigned_to.id

	def to_sql(self):
		return (self.team.id, self.assigned_to.id, self.assigner.id, self.status)
