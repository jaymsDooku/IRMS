class Stage:

	IDENTIFYING = "Identifying Resolution"
	RESOLVING = "Resolving"
	RESOLVED = "Resolved"

	def __init__(self, level):
		self.level = level

	def get_class(self):
		if self.level == Stage.IDENTIFYING:
			return "identifying-tag"
		elif self.level == Stage.RESOLVING:
			return "resolving-tag"
		else:
			return "resolved-tag"

	def to_sql(self):
		return (self.level, )