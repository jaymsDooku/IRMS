class Team:

	DERIVATIVES = "Derivatives"
	INVESTMENT = "Investment"
	MORTGAGES = "Mortgages"

	ADMIN = "Administration"
	
	RECRUITMENT = "Recruitment"
	TRAINING = "Training"

	INCIDENT_RESPONSE = "Incident Response"
	NETWORKING = "Networking"
	MAINTENANCE = "Maintenance"

	def __init__(self, name, department):
		self.name = name
		self.department = department

	def to_sql(self):
		return (self.name, self.department.id)