class UserSession:

	def __init__(self, user):
		self.user = user

	def to_sql(self):
		return (self.user.id, )
