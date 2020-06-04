class UserNotification:

	def __init__(self, user, notification, seen):
		self.user = user
		self.notification = notification
		self.seen = seen

	def to_sql(self):
		return (self.user.id, self.notification.id)