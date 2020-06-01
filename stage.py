class Stage:

	IDENTIFYING = "Identifying Resolution"
	RESOLVING = "Resolving"
	RESOLVED = "Resolved"

	def __init__(self, level):
		self.level = level

	def to_sql(self):
		return (self.level, )