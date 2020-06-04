class Severity:

	S1 = 'S1'
	S2 = 'S2'
	S3 = 'S3'

	def __init__(self, code):
		self.code = code

	def get_class(self):
		if self.code == Severity.S1:
			return 'severity-1-tag'
		elif self.code == Severity.S2:
			return 'severity-2-tag'
		else:
			return 'severity-3-tag'

	def to_sql(self):
		return (self.code, )