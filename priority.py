class Priority:

	P1 = 'P1'
	P2 = 'P2'
	P3 = 'P3'

	def __init__(self, code):
		self.code = code

	def get_class(self):
		if self.code == Priority.P1:
			return 'priority-1-tag'
		elif self.code == Priority.P2:
			return 'priority-2-tag'
		else:
			return 'priority-3-tag'

	def to_sql(self):
		return (self.code, )