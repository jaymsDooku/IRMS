class Impact:

	IMP1 = 'IMP1'
	IMP2 = 'IMP2'
	IMP3 = 'IMP3'

	def __init__(self, level):
		self.level = level

	def to_sql(self):
		return (self.level, )