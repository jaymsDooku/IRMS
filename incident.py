class Incident:

	def __init__(self, entity_manager, title, description, author, \
			sla_identification_time, sla_implementation_time, \
			status, system, impact, priority):
		self.entity_manager = entity_manager
		self.title = title
		self.description = description
		self.author = author
		self.sla_identification_time = sla_identification_time
		self.sla_implementation_time = sla_implementation_time
		self.status = status
		self.system = system
		self.impact = impact
		self.priority = priority

	def is_following(self, user):
		return self.entity_manager.is_following(user, self)

	def to_sql(self):
		return (self.title, self.description, self.author.id, \
			self.sla_identification_time, self.sla_implementation_time, \
			self.status.id, self.system.id, self.impact.id, self.priority.id)
