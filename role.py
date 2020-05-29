class Role:

	MAJOR_INCIDENT_MANAGER = "Major Incident Manager"
	SERVICE_DESK = "Service Desk"
	TECHNICIAN = "Technician"
	RESOLVER = "Resolver"
	BASIC_USER = "Basic User"
	QUEUE_MANAGER = "Queue Manager"

	def __init__(self, role_name, customer_facing):
		self.role_name = role_name
		self.customer_facing = customer_facing

	def to_sql(self):
		return (self.role_name, self.customer_facing)