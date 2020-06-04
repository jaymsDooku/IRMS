class Impact:

	IMP1 = 'IMP1'
	IMP2 = 'IMP2'
	IMP3 = 'IMP3'

	def __init__(self, level):
		self.level = level

	def get_class(self):
		if self.level == Impact.IMP1:
			return 'priority-1-tag'
		elif self.level == Impact.IMP2:
			return 'priority-2-tag'
		elif self.level == Impact.IMP3:
			return 'priority-3-tag'

	def to_sql(self):
		return (self.level, )