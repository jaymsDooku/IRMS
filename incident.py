from datetime import datetime

class Incident:

	def __init__(self, entity_manager, title, description, author, \
			sla_identification_deadline, sla_implementation_deadline, \
			status, system, impact, priority):
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

	def is_following(self, user):
		return self.entity_manager.is_following(user, self)

	def get_date_created(self):
		if self.date_created is None:
			return None

		return datetime.strptime(self.date_created, '%Y-%m-%d %H:%M:%S')

	'''def get_sla_identification_deadline(self):
		date_created_obj = self.get_date_created()

		if self.date_created is None:
			return None

		sla_identification_deadline = date_created_obj + datetime.timedelta(milliseconds=self.sla_identification_time)
		return sla_identification_deadline

	def get_sla_implementation_deadline(self):
		date_created_obj = self.get_date_created()

		if self.date_created is None:
			return

		sla_implementation_time = date_created_obj + datetime.timedelta(milliseconds=self.sla_implementation_time)
		return sla_implementation_time'''

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
		print('sla_identification_time: ' + str(self.sla_identification_time))
		print('sla_implementation_time: ' + str(self.sla_implementation_time))
		print('status: ' + str(self.status))
		print('system: ' + str(self.system))
		print('impact: ' + str(self.impact))
		print('priority: ' + str(self.priority))

	def to_sql(self):
		return (self.title, self.description, self.author.id, \
			self.sla_identification_deadline, self.sla_implementation_deadline, \
			self.status.id, self.system.id, self.impact.id, self.priority.id)
