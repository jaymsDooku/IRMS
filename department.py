class Department:

	GENERAL_MANAGEMENT = "General Management"
	FINANCIAL_SERVICES = "Financial Services"
	HUMAN_RESOURCES = "Human Resources"
	IT_SUPPORT = "IT Support"

	def __init__(self, name):
		self.name = name

	def to_sql(self):
		return (self.name,)