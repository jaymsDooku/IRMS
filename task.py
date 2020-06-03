class Task:

	def __init__(self, title, author, content, status):
		self.title = title
		self.author = author
		self.content = content
		self.status = status
		self.teams = []

	def teams_count(self):
		return len(self.teams)

	def to_sql(self):
		return (self.title, self.author.id, self.content, self.status)