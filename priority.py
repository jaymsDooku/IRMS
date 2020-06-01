class Priority:

	P1 = 'P1'
	P2 = 'P2'
	P3 = 'P3'
	S1 = 'S1'
	S2 = 'S2'
	S3 = 'S3'

	def __init__(self, code):
		self.code = code

	def to_sql(self):
		return (self.code, )