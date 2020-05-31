class Role:

	MAJOR_INCIDENT_MANAGER = "Major Incident Manager"
	SERVICE_DESK = "Service Desk"
	TECHNICIAN = "Technician"
	RESOLVER = "Resolver"
	BASIC_USER = "Basic User"
	QUEUE_MANAGER = "Queue Manager"

	def __init__(self, name, customer_facing):
		self.name = name
		self.customer_facing = customer_facing

	def to_sql(self):
		return (self.name, self.customer_facing)