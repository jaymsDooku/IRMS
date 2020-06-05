from datetime import datetime
from incident_value_change_request import IncidentValueChangeRequest
from stage import Stage

class Incident:

	def __init__(self, entity_manager, title, description, author, \
			sla_identification_deadline, sla_implementation_deadline, \
			status, system, impact, priority, severity):
		self.entity_manager = entity_manager
		self.title = title
		self.description = description
		self.author = author
		self.sla_identification_deadline = sla_identification_deadline
		self.sla_implementation_deadline = sla_implementation_deadline
		self.status = status
		self.system = system
		self.impact = impact
		self.priority = priority
		self.severity = severity
		self.notes = []
		self.questions = []
		self.tasks = []

	def is_following(self, user):
		return self.entity_manager.is_following(user, self)

	def get_on_behalf(self):
		return self.entity_manager.get_on_behalf(self)

	def is_on_behalf(self):
		return self.get_on_behalf() is not None

	def get_date_created(self):
		if self.date_created is None:
			return None

		if isinstance(self.date_created, str):
			return datetime.strptime(self.date_created, '%Y-%m-%d %H:%M:%S')
		else:
			return self.date_created

	def has_priority_change_request(self):
		change_requests = self.entity_manager.get_incident_change_requests(self)
		for change_request in change_requests:
			if change_request.value_type == IncidentValueChangeRequest.TYPE_PRIORITY and change_request.status == IncidentValueChangeRequest.STATUS_PENDING:
				return True
		return False

	def has_impact_change_request(self):
		change_requests = self.entity_manager.get_incident_change_requests(self)
		for change_request in change_requests:
			if change_request.value_type == IncidentValueChangeRequest.TYPE_IMPACT and change_request.status == IncidentValueChangeRequest.STATUS_PENDING:
				return True
		return False

	def has_severity_change_request(self):
		change_requests = self.entity_manager.get_incident_change_requests(self)
		for change_request in change_requests:
			if change_request.value_type == IncidentValueChangeRequest.TYPE_SEVERITY and change_request.status == IncidentValueChangeRequest.STATUS_PENDING:
				return True
		return False

	def get_sla_identification_time_left(self):
		date_created_obj = self.get_date_created()

		if date_created_obj is None:
			return None

		diff = self.sla_identification_deadline - date_created_obj
		return diff

	def get_sla_implementation_time_left(self):
		date_created_obj = self.get_date_created()

		if date_created_obj is None:
			return None

		diff = self.sla_implementation_deadline - date_created_obj
		return diff



	def dump(self):
		print('title: ' + str(self.title))
		print('description: ' + str(self.description))
		print('author: ' + str(self.author))
		print('sla_identification_deadline: ' + str(self.sla_identification_deadline))
		print('sla_implementation_deadline: ' + str(self.sla_implementation_deadline))
		print('status: ' + str(self.status))
		print('system: ' + str(self.system))
		print('impact: ' + str(self.impact))
		print('priority: ' + str(self.priority))

	def to_csv(self, writer):
		author_name = self.author.forename + ' ' + self.author.surname
		if self.status.level == Stage.IDENTIFYING:
			writer.writerow(["ID", "Title", "Description", "Author", "SLA Identification Deadline", \
	        	"SLA Implementation Deadline", "Status", "System", "Impact", "Priority", "Severity", "Note Count", \
	        	"Question Count", "Task Count"])
			writer.writerow([self.id, self.title, self.description, author_name, self.sla_identification_deadline, self.sla_implementation_deadline, \
				self.status.level, self.system.name, self.impact.level, self.priority.code, self.severity.code, len(self.notes), len(self.questions), len(self.tasks)])
		elif self.status.level == Stage.RESOLVING:
			writer.writerow(["ID", "Title", "Description", "Author", "SLA Identification Deadline", "Date Identified", \
	        	"SLA Implementation Deadline", "Status", "System", "Impact", "Priority", "Severity", "Note Count", \
	        	"Question Count", "Task Count"])
			writer.writerow([self.id, self.title, self.description, author_name, self.sla_identification_deadline, self.date_identified, self.sla_implementation_deadline, \
				self.status.level, self.system.name, self.impact.level, self.priority.code, self.severity.code, len(self.notes), len(self.questions), len(self.tasks)])
		elif self.status.level == Stage.RESOLVED:
			writer.writerow(["ID", "Title", "Description", "Author", "SLA Identification Deadline", "Date Identified", \
	        	"SLA Implementation Deadline", "Date Implemented", "Status", "System", "Impact", "Priority", "Severity", "Note Count", \
	        	"Question Count", "Task Count"])
			writer.writerow([self.id, self.title, self.description, author_name, self.sla_identification_deadline, self.date_identified, self.sla_implementation_deadline, self.date_implemented, \
				self.status.level, self.system.name, self.impact.level, self.priority.code, self.severity.code, len(self.notes), len(self.questions), len(self.tasks)])

	def to_sql(self):
		result = (self.title, self.description, self.author.id, \
			self.sla_identification_deadline, self.sla_implementation_deadline, \
			self.status.id, self.system.id, self.impact.id, self.severity.id, self.priority.id)
		return result
